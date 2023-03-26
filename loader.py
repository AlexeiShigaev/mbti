from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from config import TELEBOT_TOKEN

storage = StateMemoryStorage()
bot = TeleBot(TELEBOT_TOKEN, state_storage=storage)
