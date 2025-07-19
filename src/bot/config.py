import os

from dotenv import load_dotenv

load_dotenv()
# для базы данных
# DB = os.getenv('POSTGRES_DB')
# USER = os.getenv('POSTGRES_USER')
# PASSWORD = os.getenv('POSTGRES_PASSWORD')
# HOST = os.getenv('POSTGRES_HOST')
# PORT = os.getenv('POSTGRES_PORT')
# DATABASE_URL = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
# для телеграмм
BOT_API_TOKEN = os.getenv('BOT_API_TOKEN')
ADMINS = os.getenv('ADMINS')
API_URL = os.getenv('API_URL')
# Путь для сохранения файлов
# PHOTO_SAVE_PATH = 'scr/photos'
# TEXT_SAVE_PATH = 'scr/text'