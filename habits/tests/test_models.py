import datetime
from django.test import TestCase
from habits.models import UsefulHabit
from users.models import User
from django.utils import timezone


class UsefulHabitModelTest(TestCase):

    def setUp(self):
        # Создаем пользователя с паролем
        self.user = User.objects.create_user(
            email="testuser@example.com", password="password123"
        )

    def test_create_useful_habit(self):
        # Используем фиксированное время для теста
        fixed_time = timezone.make_aware(datetime.datetime(2024, 12, 23, 12, 0, 0))

        habit = UsefulHabit.objects.create(
            user=self.user, action="Test Habit", time=fixed_time, duration=30
        )

        # Проверяем правильность сохраненных данных
        self.assertEqual(habit.user.email, "testuser@example.com")
        self.assertEqual(habit.action, "Test Habit")
        self.assertEqual(habit.duration, 30)

        # Проверяем, что поле time установлено верно
        self.assertEqual(habit.time, fixed_time)
