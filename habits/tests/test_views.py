from rest_framework.test import APIClient
from django.urls import reverse
from django.test import TestCase
from users.models import User
from habits.models import Habit, Reward
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
import datetime


class HabitViewSetTest(TestCase):

    def setUp(self):
        """Подготовка данных перед тестами."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        self.other_user = User.objects.create_user(
            email="otheruser@example.com", password="testpassword"
        )

        # Генерация токена
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.url = reverse("habits:habit-list")  # Актуальный маршрут для Habit

    def test_create_pleasant_habit_with_all_fields(self):
        """Тест создания приятной привычки с обязательными полями."""
        data = {
            "action": "Read a book",
            "time": "15:30:00",
            "place": "Living room",
            "duration": 30,
            "periodicity": 1,
            "is_public": True,
            "is_pleasant_habit": True,
        }
        response = self.client.post(self.url, data, format="json")
        print(response.data)  # Распечатываем ответ для отладки
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["action"], "Read a book")
        self.assertTrue(response.data["is_pleasant_habit"])

    def test_update_habit_with_all_fields(self):
        """Тест обновления привычки с обязательными полями."""
        habit = Habit.objects.create(
            user=self.user,  # Указываем пользователя
            action="Yoga",
            time=timezone.now().time(),
            place="Gym",
            duration=30,
            periodicity=1,
            is_public=True,
        )
        url = reverse("habits:habit-detail", kwargs={"pk": habit.id})

        updated_data = {
            "action": "Morning Yoga",
            "time": "06:30:00",
            "place": "Gym",
            "duration": 40,
            "periodicity": 1,
            "is_public": True,
            "is_pleasant_habit": True,
        }

        response = self.client.put(url, updated_data, format="json")
        print(response.data)  # Распечатываем ответ для отладки
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["action"], "Morning Yoga")
        self.assertEqual(response.data["duration"], 40)
        self.assertEqual(response.data["time"], "06:30:00")
