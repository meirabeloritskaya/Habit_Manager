from django.contrib import admin
from django.contrib.auth import get_user_model
from habits.models import UsefulHabit, PleasantHabit, Reward

User = get_user_model()


class UsefulHabitInline(admin.TabularInline):
    model = UsefulHabit
    fields = (
        "action",
        "time",
        "place",
        "reward",
        "periodicity",
        "duration",
        "is_public",
    )
    extra = 0
    can_delete = True
    show_change_link = True


class PleasantHabitInline(admin.TabularInline):
    model = PleasantHabit
    fields = ("action", "is_reward", "related_useful_habit")
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
    inlines = [UsefulHabitInline, PleasantHabitInline, RewardInline]

    # Поля для редактирования в форме пользователя
    fieldsets = (
        (None, {"fields": ("email", "first_name", "last_name", "password")}),
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
