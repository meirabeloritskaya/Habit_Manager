from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Habit(models.Model):
    # Пользователь, создавший привычку
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="habits")

    # Место выполнения привычки
    place = models.CharField(max_length=255)

    # Время выполнения привычки
    time = models.TimeField()

    # Действие, которое будет выполняться
    action = models.CharField(max_length=255)

    # Признак приятной привычки
    is_pleasant = models.BooleanField(default=False)

    # Связанная привычка (для полезных привычек)
    related_habit = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,
                                      related_name="related_to")

    # Периодичность привычки (по умолчанию - 1 день)
    frequency = models.PositiveIntegerField(default=1)  # Частота в днях

    # Вознаграждение (для полезных привычек)
    reward = models.CharField(max_length=255, null=True, blank=True)

    # Время на выполнение привычки (в секундах)
    execution_time = models.PositiveIntegerField()

    # Признак публичности привычки
    is_public = models.BooleanField(default=False)

    def clean(self):
        if self.is_pleasant:
            if self.reward or self.related_habit:
                raise ValidationError('Приятная привычка не может иметь вознаграждение или связанную привычку.')
        elif self.reward and self.related_habit:
            raise ValidationError('Запрещено одновременно указывать вознаграждение и связанную привычку.')

        if self.execution_time > 120:
            raise ValidationError('Время на выполнение привычки не может быть больше 120 секунд.')

        if self.frequency < 1 or self.frequency > 7:
            raise ValidationError('Периодичность выполнения привычки должна быть от 1 до 7 дней.')

        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError('Связанная привычка должна быть приятной.')

    def __str__(self):
        return f"{self.user.username} - {self.action} в {self.place} в {self.time}"

