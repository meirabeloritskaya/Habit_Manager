import datetime
from django.test import TestCase
from habits.models import Habit, Reward
from users.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError


class HabitModelTest(TestCase):

    def setUp(self):
        """Подготовка данных перед каждым тестом."""
        self.user = User.objects.create_user(
            email="testuser@example.com", password="password123"
        )
        self.reward = Reward.objects.create(
            user=self.user, description="Test Reward", cost=50.00
        )

    def test_create_pleasant_habit(self):
        """Тест создания приятной привычки."""
        habit = Habit.objects.create(
            user=self.user,
            action="Пить чай",
            time=timezone.make_aware(datetime.datetime(2024, 12, 23, 12, 0, 0)),
            place="Кухня",
            periodicity=1,
            duration=30,  # duration обязательно
            is_public=True,
            is_pleasant_habit=True,
            reward=None,  # Приятная привычка не должна иметь вознаграждения
            related_habit=None,  # Приятная привычка не должна быть связана с другой
        )

        self.assertEqual(habit.user.email, "testuser@example.com")
        self.assertEqual(habit.action, "Пить чай")
        self.assertTrue(habit.is_pleasant_habit)
        self.assertIsNone(habit.reward)
        self.assertIsNone(habit.related_habit)

    def test_create_unpleasant_habit_with_reward(self):
        """Тест создания неприятной привычки с вознаграждением."""
        habit = Habit.objects.create(
            user=self.user,
            action="Убирать комнату",
            time=timezone.make_aware(datetime.datetime(2024, 12, 23, 15, 0, 0)),
            place="Комната",
            periodicity=2,
            duration=45,  # duration обязательно
            is_public=False,
            is_pleasant_habit=False,
            reward=self.reward,  # Неприятная привычка может иметь вознаграждение
            related_habit=None,  # Неприятная привычка может быть не связана с другой
        )

        self.assertEqual(habit.user.email, "testuser@example.com")
        self.assertEqual(habit.action, "Убирать комнату")
        self.assertFalse(habit.is_pleasant_habit)
        self.assertEqual(habit.reward.description, "Test Reward")

    def test_unpleasant_habit_with_invalid_related_habit(self):
        """Тест валидации: неприятная привычка может быть связана только с приятной привычкой."""
        pleasant_habit = Habit.objects.create(
            user=self.user,
            action="Читать книгу",
            time=timezone.now(),
            place="Гостиная",
            is_pleasant_habit=True,
            reward=None,  # Убедитесь, что для этой привычки нет вознаграждения
            related_habit=None,  # Привычка не должна быть связана с другой
            duration=30,  # duration обязательно
        )

        habit = Habit(
            user=self.user,
            action="Убирать комнату",
            time=timezone.now(),
            place="Комната",
            is_pleasant_habit=False,
            related_habit=pleasant_habit,  # Неприятная привычка может быть связана с приятной
            duration=45,  # duration обязательно
        )

        habit.full_clean()  # Проверка, что валидируется правильно

        self.assertEqual(
            habit.related_habit, pleasant_habit
        )  # Связана с приятной привычкой

    def test_create_pleasant_habit_with_invalid_reward(self):
        """Тест валидации: приятная привычка не может иметь вознаграждение."""
        habit = Habit(
            user=self.user,
            action="Читать книгу",
            time=timezone.now(),
            place="Гостиная",
            periodicity=1,
            duration=30,
            is_public=True,
            is_pleasant_habit=True,
            reward=self.reward,  # Приятная привычка не может иметь вознаграждение
            related_habit=None,  # Приятная привычка не должна быть связана с другой
        )

        with self.assertRaises(ValidationError) as context:
            habit.full_clean()  # Используйте full_clean для валидации модели

        self.assertIn(
            "Приятная привычка не может иметь вознаграждение или связанную привычку.",
            str(context.exception),
        )
