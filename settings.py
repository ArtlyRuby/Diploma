import os

from dotenv import load_dotenv

load_dotenv()

class Setting:
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_url = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}/{db_name}" # Данные можно убрать в ENV, но для локалки норм
    bot_token = os.getenv('BOT_TOKEN')
