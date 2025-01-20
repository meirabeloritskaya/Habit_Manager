from django.urls import path, include
from rest_framework.routers import DefaultRouter
from habits.views import HabitViewSet, RewardViewSet, SendReminderView
from . import views

app_name = "habits"

# Регистрируем новый ViewSet для привычек и вознаграждений
router = DefaultRouter()
router.register(r"habits", HabitViewSet, basename="habit")  # Для работы с привычками
router.register(r"rewards", RewardViewSet, basename="reward")  # Для работы с наградами

urlpatterns = [
    path("", views.home, name="home"),
    path("", include(router.urls)),  # Все маршруты для Habit и Reward через router
    path(
        "send_reminder/", SendReminderView.as_view(), name="send_reminder"
    ),  # Эндпоинт для отправки напоминаний
]
