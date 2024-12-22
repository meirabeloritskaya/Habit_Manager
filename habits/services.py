import requests
import logging
from config import settings

logger = logging.getLogger(__name__)


def send_telegram_message(chat_id, message):
    telegram_token = settings.TELEGRAM_TOKEN
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    params = {
        "text": message,
        "chat_id": chat_id,
    }
    try:
        response = requests.post(url, data=params)
        logger.info(f"Telegram response: {response.json()}")
        return response.json()
    except Exception as e:
        logger.error(f"Error sending message to Telegram: {str(e)}")
        return {"error": str(e)}
