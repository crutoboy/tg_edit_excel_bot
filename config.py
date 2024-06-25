import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN') # токен телеграм бота
EXCEL_PATH = os.getenv('EXCEL_PATH') # путь до редактируемой таблицы
