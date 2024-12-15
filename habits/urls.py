from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsefulHabitViewSet

router = DefaultRouter()
router.register(r'useful_habits', UsefulHabitViewSet, basename="useful_habit")  # Регистрация маршрута для полезных привычек

app_name = "habits"

urlpatterns = [
    path('', include(router.urls)),  # Все маршруты для полезных привычек
    path('auth/', include('users.urls')),  # Добавляем маршруты для аутентификации и регистрации пользователей
]
