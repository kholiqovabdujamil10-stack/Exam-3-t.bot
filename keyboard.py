from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎫 Мои тикеты"),KeyboardButton(text="➕ Новый тикет")],
        [KeyboardButton(text="🆘 Помощь")]
    ],
    resize_keyboard=True
)