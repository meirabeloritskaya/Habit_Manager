from django.db import models
from django.conf import settings
from rest_framework.exceptions import ValidationError


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Пользователь, который создает привычку",
    )
    action = models.CharField(
        max_length=255,
        verbose_name="Действие",
        help_text="Описание действия привычки",
    )
    time = models.TimeField(
        verbose_name="Время выполнения",
        help_text="Время, когда необходимо выполнять привычку",
    )
    place = models.CharField(
        max_length=255,
        verbose_name="Место выполнения",
        help_text="Место, где будет выполняться привычка",
    )
    reward = models.ForeignKey(
        "Reward",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Вознаграждение",
        help_text="Вознаграждение, которое пользователь получит за выполнение привычки",
    )
    related_habit = models.ForeignKey(
        "self",  # Ссылаемся на саму модель
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанная привычка",
        help_text="Привычка, которая будет связана с этой",
    )
    periodicity = models.PositiveIntegerField(
        default=1,
        verbose_name="Периодичность (в днях)",
        help_text="Периодичность повторения привычки (по умолчанию 1 день)",
    )
    duration = models.PositiveIntegerField(
        verbose_name="Время выполнения (в секундах)",
        help_text="Ожидаемое время на выполнение привычки в секундах",
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Публичность",
        help_text="Может ли привычка быть опубликована для других пользователей?",
    )
    is_pleasant_habit = models.BooleanField(
        default=False,
        verbose_name="Признак приятной привычки",
        help_text="Является ли привычка приятной",
    )

    def __str__(self):
        return self.action

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def clean(self):
        if self.is_pleasant_habit:
            # Приятная привычка не может иметь вознаграждение или связанную привычку
            if self.reward or self.related_habit:
                raise ValidationError(
                    "Приятная привычка не может иметь вознаграждение или связанную привычку."
                )
        else:  # Если привычка неприятная
            # Неприятная привычка не может иметь одновременно вознаграждение и связанную привычку
            if self.reward and self.related_habit:
                raise ValidationError(
                    "Неприятная привычка не может иметь одновременно вознаграждение и связанную привычку."
                )

            # Неприятная привычка может быть связана только с приятной
            if self.related_habit and not self.related_habit.is_pleasant_habit:
                raise ValidationError(
                    "Неприятная привычка может быть связана только с приятной."
                )


class Reward(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Пользователь, который получит вознаграждение",
    )
    description = models.CharField(
        max_length=255,
        verbose_name="Описание вознаграждения",
        help_text="Описание вознаграждения, которое пользователь получит",
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Стоимость вознаграждения",
        help_text="Стоимость вознаграждения (если применимо)",
    )

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Вознаграждение"
        verbose_name_plural = "Вознаграждения"
