import asyncio
import telebot.async_telebot as telebot
from telebot import types
import file_work as fw
from config import BOT_TOKEN


bot = telebot.AsyncTeleBot(BOT_TOKEN)

BUTTON_LABELS = {
    "view_edit": "👀 Посмотреть/Изменить таблицу",
    "download": "📥 Скачать таблицу",
    "upload": "📤 Загрузить таблицу"
}

def create_custom_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    buttons = [types.KeyboardButton(label) for label in BUTTON_LABELS.values()]
    keyboard.add(*buttons)
    return keyboard

@bot.message_handler(commands=['start', 'help'])
async def handle_start_help(message):
    custom_keyboard = create_custom_keyboard()
    await bot.send_message(message.chat.id, "Hello, how can I help you?", reply_markup=custom_keyboard)

@bot.message_handler(func=lambda message: message.text == BUTTON_LABELS["view_edit"])
async def handle_view_edit(message):
    await bot.send_message(message.chat.id, "Вы выбрали: Посмотреть/Изменить таблицу")

@bot.message_handler(func=lambda message: message.text == BUTTON_LABELS["download"])
async def handle_download(message):
    await bot.send_message(message.chat.id, "Вы выбрали: Скачать таблицу")

@bot.message_handler(func=lambda message: message.text == BUTTON_LABELS["upload"])
async def handle_upload(message):
    await bot.send_message(message.chat.id, "Вы выбрали: Загрузить таблицу")


if __name__ == '__main__':
    asyncio.run(bot.infinity_polling())
