from habits.services import send_telegram_message
from users.models import User
from celery import shared_task


@shared_task
def send_user_telegram_message(email):
    """Асинхронная задача для отправки сообщения пользователю Telegram"""

    message = "Пришло время для выполнения вышей полезной привычки"
    user = User.objects.get(email=email)
    if user.tg_chat_id:
        send_telegram_message(user.tg_chat_id, message)
