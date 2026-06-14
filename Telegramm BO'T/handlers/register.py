import re
from telebot.types import Message, CallbackQuery, ReplyKeyboardRemove
from config.bot import bot
from config.settings import GROUP_ID
from buttons import reply as btn
from states import register_state as states
from utils import text as txt

@bot.callback_query_handler(func=lambda d: d.data == "register_btn")
def handler_start_btn(query: CallbackQuery):
    bot.set_state(query.from_user.id, states.Register.fio, query.message.chat.id)
    bot.send_message(query.message.chat.id, "Ism familiyangizni kiriting")

@bot.message_handler(content_types=["text"], state=states.Register.fio)
def handler_fio(message: Message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data: data["fio"] = message.text
    bot.set_state(message.from_user.id, states.Register.age, message.chat.id)
    bot.send_message(message.chat.id, "Yoshingizni kiriting", reply_markup=ReplyKeyboardRemove())

@bot.message_handler(content_types=["text"], state=states.Register.age)
def handler_age(message: Message):
    age = message.text
    if age.isdigit():
        age = int(age)
        if 11 <= age <= 30:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data: data["age"] = age
            bot.set_state(message.from_user.id, states.Register.course, message.chat.id)
            bot.send_message(message.chat.id, "Kurslardan birini tanlang", reply_markup=btn.courses())
        else: bot.send_message(message.chat.id, "Kechirasiz, bizni kurslar 11-30 yoshgacha mo'ljallangan.")
    else: bot.send_message(message.chat.id, "Yoshingizni faqat raqam ko'rinishida yuboring (Masalan: 18)")

@bot.message_handler(content_types=["text"], state=states.Register.course)
def handler_course(message: Message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data: data["course"] = message.text
    bot.set_state(message.from_user.id, states.Register.contact, message.chat.id)
    bot.send_message(message.chat.id, "Telefon raqamingizni yuboring pastdagi tugma orqali", reply_markup=btn.share_contact())

@bot.message_handler(content_types=["text", "contact"], state=states.Register.contact)
def handler_contact(message: Message):
    user_id, chat_id = message.from_user.id, message.chat.id
    if message.text:
        if re.match(r"^\+?998[3789][012345789]\d{7}$", message.text):
            with bot.retrieve_data(user_id, chat_id) as data: data["contact"] = message.text
            bot.set_state(user_id, states.Register.address, chat_id)
            bot.send_message(chat_id, "Yashash manzilingizni yuboring", reply_markup=btn.share_location())
        else: bot.send_message(chat_id, "Iltimos, telefon raqamni to'g'ri formatda kiriting yoki tugmani bosing")
    elif message.contact:
        with bot.retrieve_data(user_id, chat_id) as data: data["contact"] = message.contact.phone_number
        bot.set_state(user_id, states.Register.address, chat_id)
        bot.send_message(chat_id, "Yashash manzilingizni yuboring", reply_markup=btn.share_location())

@bot.message_handler(content_types=["text", "location"], state=states.Register.address)
def handler_address(message: Message):
    user_id, chat_id = message.from_user.id, message.chat.id
    with bot.retrieve_data(user_id, chat_id) as data:
        if message.location:
            data["latitude"], data["longitude"] = message.location.latitude, message.location.longitude
            data["address"] = "Location"
        else: data["address"] = message.text
    bot.set_state(user_id, states.Register.study_time, chat_id)
    bot.send_message(chat_id, "O'qish vaqtini tanlang", reply_markup=btn.study_time())

@bot.message_handler(content_types=["text"], state=states.Register.study_time)
def handler_study_time(message: Message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data: data["study_time"] = message.text
    bot.set_state(message.from_user.id, states.Register.document, message.chat.id)
    bot.send_message(message.chat.id, "Fayl (passport/metrika) yuboring", reply_markup=ReplyKeyboardRemove())

@bot.message_handler(content_types=["document", "photo", "text"], state=states.Register.document)
def handler_document(message: Message):
    user_id, chat_id = message.from_user.id, message.chat.id
    valid = False
    with bot.retrieve_data(user_id, chat_id) as data:
        if message.photo:
            data["document"] = message.photo[-1].file_id
            data["file_type"] = "photo"
            valid = True
        elif message.document and message.document.file_name.endswith(".pdf"):
            data["document"] = message.document.file_id
            data["file_type"] = "document"
            valid = True
    if valid:
        bot.set_state(user_id, states.Register.confirmation, chat_id)
        bot.send_message(chat_id, txt.generate_text(data), parse_mode="HTML")
        bot.send_message(chat_id, "Barcha ma'lumotlar to'g'rimi?", reply_markup=btn.confirm())
    else: bot.send_message(chat_id, "Iltimos, rasm yoki PDF formatidagi fayl yuboring.")

@bot.message_handler(content_types=["text"], state=states.Register.confirmation)
def handler_confirmation(message: Message):
    user_id, chat_id = message.from_user.id, message.chat.id
    if message.text == "Ha":
        with bot.retrieve_data(user_id, chat_id) as data:
            info = txt.generate_text(data)
            if data["file_type"] == "photo": bot.send_photo(GROUP_ID, data["document"], caption=info, parse_mode="HTML")
            elif data["file_type"] == "document": bot.send_document(GROUP_ID, data["document"], caption=info, parse_mode="HTML")
        bot.send_message(chat_id, "Tabriklaymiz, ro'yxatdan o'tdingiz!", reply_markup=ReplyKeyboardRemove())
        bot.delete_state(user_id, chat_id)
    elif message.text == "Yo'q":
        bot.send_message(chat_id, "Bekor qilindi. Qayta boshlash: /start", reply_markup=ReplyKeyboardRemove())
        bot.delete_state(user_id, chat_id)