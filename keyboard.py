from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎫 Мои тикеты"),KeyboardButton(text="➕ Новый тикет")]],
        resize_keyboard=True
    )