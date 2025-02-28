from django.contrib import admin
from django.contrib.auth import get_user_model
from habits.models import Habit, Reward

User = get_user_model()


class HabitInline(admin.TabularInline):
    model = Habit
    fields = (
        "action",
        "time",
        "place",
        "reward",
        "is_pleasant_habit",  # Новый флаг для отличия полезной и приятной привычки
        "periodicity",
        "duration",
        "is_public",
    )
    extra = 0
    can_delete = True
    show_change_link = True


class RewardInline(admin.TabularInline):
    model = Reward
    fields = ("description", "cost")
    extra = 0
    can_delete = True
    show_change_link = True


# Настройки для пользователя
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "first_name", "last_name", "is_active", "is_staff")
    list_filter = ("is_active", "is_staff", "is_superuser", "groups")
    search_fields = ("first_name", "last_name", "email")
    ordering = ["email"]

    # Добавляем инлайны для отображения связанных моделей
    inlines = [HabitInline, RewardInline]

    # Поля для редактирования в форме пользователя
    fieldsets = (
        (
            None,
            {"fields": ("email", "tg_chat_id", "first_name", "last_name", "password")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    # Добавляем поля для создания нового пользователя
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_active", "is_staff"),
            },
        ),
    )
