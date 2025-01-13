import requests
import logging
from config import settings
from pytz import timezone
from datetime import datetime

logger = logging.getLogger(__name__)

jerusalem_tz = timezone("Asia/Jerusalem")


def send_telegram_message(chat_id, message):
    # Получаем текущее время в Иерусалиме
    local_time = datetime.now(jerusalem_tz).strftime("%Y-%m-%d %H:%M:%S")

    message_with_time = f"{message} (Local time: {local_time})"

    telegram_token = settings.TELEGRAM_TOKEN
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    params = {
        "text": message_with_time,
        "chat_id": chat_id,
    }
    try:
        response = requests.post(url, data=params)
        logger.info(f"Telegram response: {response.json()}")
        return response.json()
    except Exception as e:
        logger.error(f"Error sending message to Telegram: {str(e)}")
        return {"error": str(e)}
