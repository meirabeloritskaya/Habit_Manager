from django.contrib import admin
from habits.models import Habit, Reward


class HabitAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "action",
        "time",
        "place",
        "reward",
        "related_habit",  # Добавим поле для связанной привычки
        "is_pleasant_habit",
        "periodicity",
        "duration",
        "is_public",
    ]
    list_filter = [
        "is_public",
        "is_pleasant_habit",
        "periodicity",
        "reward",
        "related_habit",
    ]
    search_fields = ["action", "reward__description", "related_habit__action"]
    ordering = ["user", "action"]
    autocomplete_fields = ["reward", "related_habit"]


class RewardAdmin(admin.ModelAdmin):
    list_display = ["user", "description", "cost"]
    list_filter = ["user"]
    search_fields = ["description"]
    ordering = ["user", "description"]


# Регистрация моделей в админке
admin.site.register(Habit, HabitAdmin)
admin.site.register(Reward, RewardAdmin)
