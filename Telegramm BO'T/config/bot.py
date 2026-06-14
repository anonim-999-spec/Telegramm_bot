import telebot
from telebot.storage import StateMemoryStorage
from config.settings import API_TOKEN

bot = telebot.TeleBot(API_TOKEN, state_storage=StateMemoryStorage())
bot.add_custom_filter(telebot.custom_filters.StateFilter(bot))
bot.set_my_commands([telebot.types.BotCommand(command="start", description="Botni qayta yuklash")])