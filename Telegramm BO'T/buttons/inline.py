from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def start_btn():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Bo'tga kirish", callback_data="register_btn"))
    return markup