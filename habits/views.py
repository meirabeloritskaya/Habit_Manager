from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from habits.models import Habit, Reward  # Используем обновленную модель Habit
from habits.serializers import HabitSerializer, RewardSerializer
from rest_framework.views import APIView
from habits.permissions import IsOwnerOrReadOnly
from habits.services import send_telegram_message
from users.models import User
from users.serializers import (
    UserSerializer,
)  # Добавлен импорт сериализатора пользователя
from habits.serializers import (
    RegisterSerializer,
)  # Добавлен импорт сериализатора для регистрации
from django.http import HttpResponse

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Создаем пользователя
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ViewSet для привычек (Habit)
class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer  # Используем сериализатор для Habit
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]  # Обычные пользователи только свои привычки

    def get_queryset(self):
        """
        Возвращает публичные привычки для всех пользователей или все привычки текущего пользователя.
        Суперпользователи видят все привычки.
        """
        user = self.request.user
        if user.is_superuser:  # Если пользователь суперпользователь
            return Habit.objects.all()

        if self.action == "list":  # Запрос на получение списка привычек
            if user.is_authenticated:
                # Публичные привычки + личные привычки текущего пользователя
                return Habit.objects.filter(is_public=True) | Habit.objects.filter(
                    user=user
                )
            else:
                # Только публичные привычки для неаутентифицированных пользователей
                return Habit.objects.filter(is_public=True)

        elif self.action == "retrieve":  # Запрос на получение конкретной привычки
            # Проверка, принадлежит ли привычка текущему пользователю
            habit = Habit.objects.filter(id=self.kwargs["pk"]).first()
            if habit and habit.user != user and not user.is_superuser:
                raise PermissionDenied("У вас нет прав на просмотр этой привычки.")

        # Возвращаем только привычки текущего пользователя
        return Habit.objects.filter(user=user)

    def perform_create(self, serializer):
        """
        Устанавливаем текущего пользователя как владельца создаваемой привычки.
        """
        habit = serializer.save(user=self.request.user)

        # Проверки для приятных и неприятных привычек
        if habit.is_pleasant_habit:
            if habit.reward or habit.related_habit:
                raise PermissionDenied(
                    "Для приятной привычки нельзя указать вознаграждение или связанную привычку."
                )
        else:
            if habit.reward and habit.related_habit:
                raise PermissionDenied(
                    "Неприятная привычка не может иметь одновременно вознаграждение и связанную привычку."
                )


# ViewSet для наград (Reward)
class RewardViewSet(viewsets.ModelViewSet):
    serializer_class = RewardSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Возвращает только награды текущего пользователя.
        """
        return Reward.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Устанавливаем текущего пользователя как владельца создаваемой награды.
        """
        serializer.save(user=self.request.user)


class SendReminderView(APIView):
    """
    Класс для отправки напоминания пользователю через Telegram.
    Ожидается, что в запросе будет передан email пользователя, которому нужно отправить напоминание.
    """

    def post(self, request):
        print("Запрос получен!")
        email = request.data.get("email")
        if not email:
            print("Email не передан!")
            return Response(
                {"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            print(f"Looking for user with email: {email}")
            user = User.objects.get(email=email)
            print(f"User found: {user.email}")

            if user.tg_chat_id:
                message = "Пришло время для выполнения вашей привычки!"
                print(f"Sending message to chat_id: {user.tg_chat_id}")
                send_telegram_message(user.tg_chat_id, message)
                print(f"Сообщение отправлено пользователю {email}")
                return Response({"message": "Напоминание отправлено!"})
            else:
                print(f"У пользователя {email} нет chat_id")
                return Response(
                    {"error": "User does not have a Telegram chat ID"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except User.DoesNotExist:
            print(f"Пользователь с email {email} не найден")
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

def home(request):
    return HttpResponse("Welcome to the Materials Application!")