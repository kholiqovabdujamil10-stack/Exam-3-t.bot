
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message
from dotenv import load_dotenv
from service import *
from connection import *
from keyboard import *
import asyncio
import os


load_dotenv()
token = os.getenv("BOT_TOKEN")

bot = Bot(token=token)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_bot(message: Message):
    user = message.from_user
    user_data = await get_user(user.id)
    if user_data:
        await message.answer(f"Здарова, {user.full_name}! 😎", reply_markup=main_menu)
    else:
        status = await created_user(user.username, user.full_name, user.id)
        if status:
            await message.answer(f"Добро пожаловать, {user.full_name}, братишка! 🔥", reply_markup=main_menu)
        else:
            await message.answer("Брат, не получилось создать профиль 😭 Попробуй позже.")



@dp.message(Command("help"))
@dp.message(F.text == "🆘 Помощь")
async def help_command(message: Message):
    await message.answer(
        "🎫 SUPPORT TICKET SYSTEM 😎\n\n"
        "Братишка, здесь можно создавать тикеты и общаться с поддержкой.\n\n"
        "📌 ДОСТУПНЫЕ КОМАНДЫ:\n\n"
        "➕ /new_ticket <subject>\n"
        "Создать новый тикет, брат 🔥\n\n"
        "🎫 /my_tickets\n"
        "Посмотреть свои тикеты. Проверим, сколько у тебя дел 😂\n\n"
        "💬 /reply <ticket_id> <text>\n"
        "Написать сообщение в тикет.\n"
        "Пример: /reply 1 Не могу войти в аккаунт\n\n"
        "📜 /ticket_history <ticket_id>\n"
        "Посмотреть всю переписку.\n"
        "Пример: /ticket_history 1\n\n"
        "🔒 /close_ticket <ticket_id>\n"
        "Закрыть тикет, если проблема решена. Красиво уходим 😎\n"
        "Пример: /close_ticket 1"
    )

@dp.message(Command("new_ticket"))
async def new_ticket(message: Message, command: CommandObject):
    subject = (command.args or "").strip()
    if not subject:
        await message.answer("Братишка, сначала напиши тему тикета 😅\nПример: /new_ticket Не работает бот")
        return
    if len(subject) > 200:
        await message.answer("Опа, брат, тема слишком длинная 😂 Максимум 200 символов.")
        return
    status = await create_ticket(message.from_user.id, subject)
    if status:
        await message.answer("🎫 Братишка, тикет создан! Теперь ждём магии 🪄🔥")
    else:
        await message.answer("Не получилось создать тикет, брат. База сегодня грустит 😭")



@dp.message(Command("my_tickets"))
@dp.message(F.text == "🎫 Мои тикеты")
async def my_tickets(message: Message):
    tickets = await get_user_tickets(message.from_user.id)
    if not tickets:
        await message.answer("Братишка, у тебя пока нет тикетов. Отдыхаешь? 😂")
        return
    text = ""
    for ticket in tickets:
        status = "🟢 Open" if ticket["status"] == "open" else "🔴 Closed"
        text += (
            f"🎫 Ticket ID: {ticket['ticket_id']}\n"
            f"📝 Subject: {ticket['subject']}\n"
            f"📌 Status: {status}\n\n"
        )
    await message.answer(text)






@dp.message(Command("reply"))
async def reply_ticket(message: Message, command: CommandObject):
    data = (command.args or "").split(maxsplit=1)
    if len(data) != 2 or not data[1].strip():
        await message.answer("Брат, напиши ID тикета и сообщение 😅\nПример: /reply 1 Не работает бот")
        return
    try:
        ticket_id = int(data[0])
        if ticket_id <= 0:
            raise ValueError
    except ValueError:
        await message.answer("Братишка, ID должен быть положительным числом 😂")
        return
    ticket = await get_ticket(ticket_id)
    if not ticket:
        await message.answer("Брат, такого тикета вообще не существует 💀")
        return
    if ticket["user_id"] != message.from_user.id:
        await message.answer("Это не твой тикет, братишка 😂")
        return
    if ticket["status"] == "closed":
        await message.answer("Братишка, тикет уже закрыт. Поезд ушёл 🚂😂")
        return
    status = await add_reply(ticket_id, "user", data[1].strip())
    if status:
        await message.answer("🚀 Ответ залетел, братишка!")
    else:
        await message.answer("Брат, не получилось отправить сообщение 😭")

@dp.message(Command("ticket_history"))
async def show_ticket_history(message: Message, command: CommandObject):
    try:
        ticket_id = int((command.args or "").strip())
        if ticket_id <= 0:
            raise ValueError
    except ValueError:
        await message.answer("Брат, укажи ID тикета правильно 😅\nПример: /ticket_history 1")
        return
    ticket = await get_ticket(ticket_id)
    if not ticket:
        await message.answer("Братишка, такого тикета нет 💀")
        return
    if ticket["user_id"] != message.from_user.id:
        await message.answer("Брат, это чужая история. Не лезем 😂")
        return
    replies = await ticket_history(ticket_id)
    text = (
        f"📜 История тикета #{ticket_id}\n"
        f"📝 Тема: {ticket['subject']}\n"
        f"📌 Статус: {ticket['status']}\n"
    )
    if not replies:
        await message.answer(text + "\nТут пока тишина, братишка 🤐")
        return
    for reply in replies:
        text += f"\n{reply['author']}: {reply['message']}"
    await message.answer(text)






@dp.message(Command("close_ticket"))
async def close_user_ticket(message: Message, command: CommandObject):
    try:
        ticket_id = int((command.args or "").strip())
        if ticket_id <= 0:
            raise ValueError
    except ValueError:
        await message.answer("Братишка, укажи правильный ID тикета 😅")
        return
    ticket = await get_ticket(ticket_id)
    if not ticket:
        await message.answer("Брат, такого тикета не существует 💀")
        return
    if ticket["user_id"] != message.from_user.id:
        await message.answer("Это не твой тикет братишка 😂")
        return
    if ticket["status"] == "closed":
        await message.answer("Братишка, он уже закрыт. Хватит его мучить 😂")
        return
    status = await close_ticket(ticket_id)
    if status:
        await message.answer("🔒 Всё, братишка, тикет закрыт! Дело сделано 😎")
    else:
        await message.answer("Не получилось закрыть тикет, брат 😭")





@dp.message(F.text == "➕ Новый тикет")
async def new_ticket_button(message: Message):
    await message.answer("Братишка, напиши тему вот так:\n/new_ticket Не работает бот 😎")


async def main():
    await create_table()
    print("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())