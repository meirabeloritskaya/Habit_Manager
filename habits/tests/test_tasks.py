from django.test import TestCase
from habits.tasks import send_habit_reminders


class CeleryTaskTest(TestCase):

    def test_send_habit_reminders(self):
        result = send_habit_reminders.apply()
        self.assertEqual(
            result.status, "SUCCESS"
        )  # Проверяем успешное выполнение задачи
