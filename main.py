import telebot
from telebot import types
import file_work as fw
from config import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)

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

def start_message(message):
    custom_keyboard = create_custom_keyboard()
    bot.send_message(message.chat.id,
                     "Добро пожаловать в бота для редактирования excel-таблицы",
                     reply_markup=custom_keyboard)

@bot.message_handler(commands=['start'])
def handle_start_help(message):
    start_message()
    # user_id = message.from_user.id
    # if fw.user_is_registr(user_id):
    #     start_message(message)
    # else:
    #     bot.send_message(user_id, 'Вы не зарегистрированы. Введите своё ФИО')
    #     bot.register_next_step_handler(message, registration)

def registration(message):
    ...
    # fw.user_registration(message.from_user.id, message.text)
    # start_message(message)

def filters_to_str(header, filters) -> str:
    out = ''
    indexs = range(len(header))
    for index, head, filter in zip(indexs, header, filters):
        out += f'{index}. {head} == {filter}\n'
    return out

@bot.message_handler(func=lambda message: message.text == BUTTON_LABELS["view_edit"])
def view_filters(message, header=None, filters=None):
    if header is None:
        header = fw.get_header()
    if filters is None:
        filters = [None] * len(header)
    filters_str = fwfilters_to_str(header, filters)
    count = fw.count_select_filter_rows(filters)
    bot.send_message(message.chat.id, f"Текущие фильтры:\n\n"
                                      f"{filters_str}\n"
                                      f"Количество выбранных строк: ")
    start_filter(message)

def start_filter(message):
    rows = fw.xl_read_data()
    rows = fw.xl_filter_column_by_user(rows, message.from_user.id)
    print(len(rows))
    bot.send_message()

@bot.message_handler(func=lambda message: message.text == BUTTON_LABELS["download"])
def handle_download(message):
    bot.send_message(message.chat.id, "Вы выбрали: Скачать таблицу")

@bot.message_handler(func=lambda message: message.text == BUTTON_LABELS["upload"])
def handle_upload(message):
    bot.send_message(message.chat.id, "Вы выбрали: Загрузить таблицу")

if __name__ == '__main__':
    bot.infinity_polling()
