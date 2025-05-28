import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Paths
STORAGE_PATH = os.path.join(os.path.dirname(__file__), '..', 'storage')
METADATA_FILE = os.path.join(STORAGE_PATH, 'metadata.json')

# Server settings
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8000))

# Webhook settings (optional)
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
WEBHOOK_PATH = '/webhook'

# Video settings
MAX_VIDEO_SIZE = 50 * 1024 * 1024  # 50MB
MAX_METADATA_ENTRIES = 500  # Максимальное количество записей в metadata.json 