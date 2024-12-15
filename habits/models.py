from django.db import models
from django.conf import settings


class UsefulHabit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Пользователь, который создает привычку"
    )
    action = models.CharField(
        max_length=255,
        verbose_name="Действие",
        help_text="Описание действия, которое будет выполнено в рамках привычки"
    )
    time = models.TimeField(
        verbose_name="Время выполнения",
        help_text="Время, когда необходимо выполнять привычку"
    )
    place = models.CharField(
        max_length=255,
        verbose_name="Место выполнения",
        help_text="Место, где будет выполняться привычка"
    )
    reward = models.ForeignKey(
        'Reward',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Вознаграждение",
        help_text="Вознаграждение, которое пользователь получит за выполнение привычки"
    )
    related_habit = models.ForeignKey(
        'PleasantHabit',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанная привычка",
        help_text="Приятная привычка, которая будет связана с этой полезной привычкой"
    )
    periodicity = models.PositiveIntegerField(
        default=1,
        verbose_name="Периодичность (в днях)",
        help_text="Периодичность повторения привычки (по умолчанию 1 день)"
    )
    duration = models.PositiveIntegerField(
        verbose_name="Время выполнения (в секундах)",
        help_text="Ожидаемое время на выполнение привычки в секундах"
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Публичность",
        help_text="Может ли привычка быть опубликована для других пользователей?"
    )

    def __str__(self):
        return self.action

    class Meta:
        verbose_name = "Полезная привычка"
        verbose_name_plural = "Полезные привычки"


class PleasantHabit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Пользователь, который создает приятную привычку"
    )
    action = models.CharField(
        max_length=255,
        verbose_name="Действие",
        help_text="Описание действия приятной привычки"
    )
    is_reward = models.BooleanField(
        default=True,
        verbose_name="Признак вознаграждения",
        help_text="Является ли эта привычка способом вознаградить себя за выполнение полезной привычки"
    )
    related_useful_habit = models.ForeignKey(
        'UsefulHabit',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Связанная полезная привычка",
        help_text="Полезная привычка, с которой связана эта приятная привычка"
    )

    def __str__(self):
        return self.action

    class Meta:
        verbose_name = "Приятная привычка"
        verbose_name_plural = "Приятные привычки"


class Reward(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Пользователь, который получит вознаграждение"
    )
    description = models.CharField(
        max_length=255,
        verbose_name="Описание вознаграждения",
        help_text="Описание вознаграждения, которое пользователь получит"
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Стоимость вознаграждения",
        help_text="Стоимость вознаграждения (если применимо)"
    )

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Вознаграждение"
        verbose_name_plural = "Вознаграждения"
