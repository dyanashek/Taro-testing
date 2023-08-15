import os
from dotenv import load_dotenv

import text

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# manager's id (redirect users to him)
MANAGER_ID = os.getenv('MANAGER_ID')

# bot's ID
BOT_ID = os.getenv('BOT_ID')

# manager's username
MANAGER_USERNAME = os.getenv('MANAGER_USERNAME')

# instagram link
INSTAGRAM_LINK = os.getenv('INSTAGRAM_LINK')

# telegram channel link
TELEGRAM_CHANNEL_LINK = os.getenv('TELEGRAM_CHANNEL_LINK')

SPREAD_NAME = 'Код Таро даты рождения'
LIST_NAME = 'Тестовые расклады'

