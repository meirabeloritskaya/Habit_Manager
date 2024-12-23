from rest_framework.test import APIClient
from django.urls import reverse
from django.test import TestCase
from users.models import User
from habits.models import UsefulHabit
from rest_framework_simplejwt.tokens import RefreshToken


class HabitViewSetTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )

        # Генерация токена
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.url = reverse("habits:useful_habit-list")

    def test_get_habits(self):
        habit = UsefulHabit.objects.create(
            action="Test habit", time="15:35:00", user=self.user, duration=30
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Test habit", [habit["action"] for habit in response.data["results"]]
        )

    def test_create_habit(self):
        data = {
            "user": self.user.id,
            "action": "Test Habit",
            "time": "15:30:00",
            "place": "Home",
            "duration": 30,
            "periodicity": 1,
            "is_public": True,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, 201)
