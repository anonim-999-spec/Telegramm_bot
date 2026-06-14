from telebot.types import ReplyKeyboardMarkup, KeyboardButton

COURSES = ['Backend', 'Frontend', 'Android', 'Full Stack', 'Graphic Designing', 'Mobile Programming', 'Desktop Programming']
STUDY_TIME = ['Abettan kegin', 'abetta', 'Kechki']

def courses():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in COURSES: markup.add(KeyboardButton(text=i))
    return markup

def share_contact():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(text="Telefon raqam", request_contact=True))
    return markup

def share_location():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(text="Location", request_location=True))
    return markup

def study_time():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in STUDY_TIME: markup.add(KeyboardButton(text=i))
    return markup

def confirm():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(text="Ha"), KeyboardButton(text="Yo'q"))
    return markup