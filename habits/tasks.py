from habits.services import send_telegram_message
from django.utils import timezone
from celery import shared_task
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from habits.models import UsefulHabit
import json


@shared_task
def send_habit_reminders():
    """Отправляет напоминания о привычках в указанное пользователем время."""
    now = timezone.localtime(timezone.now())
    current_time = now.time()

    habits = UsefulHabit.objects.filter(time=current_time)
    for habit in habits:
        chat_id = habit.user.tg_chat_id
        if chat_id:
            message = f"Пора выполнить привычку: {habit.action}"
            send_telegram_message(chat_id, message)
            print(
                f"Напоминание отправлено пользователю {habit.user.email} для привычки '{habit.action}'"
            )


@shared_task
def schedule_habit_reminders():
    """Настраивает периодические задачи для привычек в Celery Beat."""
    habits = UsefulHabit.objects.all()
    for habit in habits:
        # Создаем или обновляем расписание на основе periodicity
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=habit.periodicity,
            period=IntervalSchedule.DAYS,
        )

        # Создаем или обновляем задачу для каждой привычки
        PeriodicTask.objects.update_or_create(
            name=f"habit_reminder_{habit.id}",
            defaults={
                "interval": schedule,
                "task": "habits.tasks.send_single_habit_reminder",
                "args": json.dumps([habit.id]),
            },
        )
    print("Расписание для привычек обновлено.")


@shared_task
def send_single_habit_reminder(habit_id):
    """Отправляет напоминание для одной привычки."""
    try:
        habit = UsefulHabit.objects.get(id=habit_id)
        chat_id = habit.user.tg_chat_id
        if chat_id:
            message = f"Пора выполнить привычку: {habit.action}"
            send_telegram_message(chat_id, message)
            print(
                f"Напоминание отправлено пользователю {habit.user.email} для привычки '{habit.action}'"
            )
    except UsefulHabit.DoesNotExist:
        print(f"Привычка с ID {habit_id} не найдена.")
