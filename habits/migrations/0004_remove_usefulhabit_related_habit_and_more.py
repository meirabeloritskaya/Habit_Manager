# Generated by Django 5.1.4 on 2024-12-29 04:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("habits", "0003_pleasanthabit_reward_usefulhabit_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="usefulhabit",
            name="related_habit",
        ),
        migrations.RemoveField(
            model_name="usefulhabit",
            name="reward",
        ),
        migrations.RemoveField(
            model_name="usefulhabit",
            name="user",
        ),
        migrations.CreateModel(
            name="Habit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "action",
                    models.CharField(
                        help_text="Описание действия привычки",
                        max_length=255,
                        verbose_name="Действие",
                    ),
                ),
                (
                    "time",
                    models.TimeField(
                        help_text="Время, когда необходимо выполнять привычку",
                        verbose_name="Время выполнения",
                    ),
                ),
                (
                    "place",
                    models.CharField(
                        help_text="Место, где будет выполняться привычка",
                        max_length=255,
                        verbose_name="Место выполнения",
                    ),
                ),
                (
                    "periodicity",
                    models.PositiveIntegerField(
                        default=1,
                        help_text="Периодичность повторения привычки (по умолчанию 1 день)",
                        verbose_name="Периодичность (в днях)",
                    ),
                ),
                (
                    "duration",
                    models.PositiveIntegerField(
                        help_text="Ожидаемое время на выполнение привычки в секундах",
                        verbose_name="Время выполнения (в секундах)",
                    ),
                ),
                (
                    "is_public",
                    models.BooleanField(
                        default=False,
                        help_text="Может ли привычка быть опубликована для других пользователей?",
                        verbose_name="Публичность",
                    ),
                ),
                (
                    "is_pleasant_habit",
                    models.BooleanField(
                        default=False,
                        help_text="Является ли привычка приятной",
                        verbose_name="Признак приятной привычки",
                    ),
                ),
                (
                    "related_habit",
                    models.ForeignKey(
                        blank=True,
                        help_text="Привычка, которая будет связана с этой",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="habits.habit",
                        verbose_name="Связанная привычка",
                    ),
                ),
                (
                    "reward",
                    models.ForeignKey(
                        blank=True,
                        help_text="Вознаграждение, которое пользователь получит за выполнение привычки",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="habits.reward",
                        verbose_name="Вознаграждение",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        help_text="Пользователь, который создает привычку",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Привычка",
                "verbose_name_plural": "Привычки",
            },
        ),
        migrations.DeleteModel(
            name="PleasantHabit",
        ),
        migrations.DeleteModel(
            name="UsefulHabit",
        ),
    ]
