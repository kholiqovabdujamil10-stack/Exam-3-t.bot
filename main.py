from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message
from dotenv import load_dotenv
import asyncio
import os
from connection import *
from service import *
from keyboard import *

load_dotenv()

token = os.getenv("BOT_TOKEN")

bot = Bot(token=token)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_bot(message: Message):
    user = message.from_user
    
    if await get_user(user.id):
        await message.answer(
            f"Hello, MRS | MR {user.full_name}"
        )
        await message.answer(
            f"Mr | Mrs @{user.full_name}, "
            "to see all commands enter /help",
        )
    else:
        success = await created_user(
            user.username,
            user.full_name,
            user.id
        )
        if not success:
            await message.answer("Error creating user. Try again later.")
            return
        await message.answer(
            f"Hello @{user.username or user.full_name}, how are you?",
        )


@dp.message(Command("Help"))
async def help_command(message: Message):
    await message.answer(
        "Welcome! Here are the available commands:\n\n"
        "/start — Start the bot\n"
        "/help — Show help\n"
        "/profile — View your profile\n"
        "/ticket_history — Ticket history\n"
        "/close_ticket — Closes your ticket\n"
        "/reply — Add income\n"
    )


@dp.message(Command("profile"))
async def profile(message: Message):
    print("Profile command received")
    user = await get_user(message.from_user.id)
    if not user:
        await message.answer("User not found.")
        return
    await message.answer(
        f"👤 Full Name: {user['full_name']}\n"
        f"🏷 Username: @{user['username'] or 'Not set'}\n"
    )


@dp.message(Command("history"))
async def history(message: Message):
    transactions = await ticket_history(message.from_user.id)
    if not transactions:
        await message.answer("History is empty.")
        return
    text = "Transaction History:\n\n"
    for i in transactions:
        text += (
            f"{i['operation_type']}: {i['amount']} TJS\n"
            f"Description: {i['description'] or '-'}\n\n"
        )

    await message.answer(text)
