import os

from dotenv import load_dotenv

load_dotenv()

class Setting:
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_url = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}/{db_name}"
    bot_token = os.getenv('BOT_TOKEN')
    admin_chat_id = os.getenv('ADMIN_CHAT_ID')
    admin_group_id = os.getenv('ADMIN_GROUP_ID')

