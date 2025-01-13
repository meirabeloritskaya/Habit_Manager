from django_celery_beat.models import PeriodicTask, IntervalSchedule

# Создание расписания
schedule, _ = IntervalSchedule.objects.get_or_create(
    every=1,
    period=IntervalSchedule.MINUTES,
)

# Создание периодической задачи
PeriodicTask.objects.update_or_create(
    name="Send Scheduled Reminders",
    defaults={
        "task": "habits.tasks.send_scheduled_reminders",
        "interval": schedule,
    },
)
