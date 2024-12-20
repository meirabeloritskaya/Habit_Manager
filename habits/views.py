from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from habits.models import UsefulHabit, PleasantHabit, Reward
from habits.serializers import (
    RegisterSerializer,
    UserSerializer,
    UsefulSerializer,
    PleasantHabitSerializer,
    RewardSerializer,
)
from rest_framework.views import APIView
from habits.permissions import (
    IsOwnerOrReadOnly,
)  # Используем кастомный пермишн для проверки владельца


# Вьюха для регистрации пользователя
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Создаем пользователя
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ViewSet для полезных привычек (UsefulHabit)
class UsefulHabitViewSet(viewsets.ModelViewSet):
    serializer_class = UsefulSerializer  # Сериализатор для полезных привычек
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Возвращает публичные привычки для всех пользователей или все привычки текущего пользователя.
        """
        user = self.request.user
        if self.action == "list":  # Если это запрос списка
            if user.is_authenticated:
                # Публичные привычки + личные привычки пользователя
                return UsefulHabit.objects.filter(
                    is_public=True
                ) | UsefulHabit.objects.filter(user=user)
            else:
                return UsefulHabit.objects.filter(is_public=True)
        elif self.action == "retrieve":
            # Если это запрос на получение данных о привычке, проверим, принадлежит ли она пользователю
            habit = UsefulHabit.objects.filter(id=self.kwargs["pk"]).first()
            if habit and habit.user != user:
                raise PermissionDenied("У вас нет прав на просмотр этой привычки.")
        return UsefulHabit.objects.filter(user=user)

    def perform_create(self, serializer):
        """
        Устанавливаем текущего пользователя как владельца создаваемой привычки.
        """
        serializer.save(user=self.request.user)


# ViewSet для приятных привычек (PleasantHabit)
class PleasantHabitViewSet(viewsets.ModelViewSet):
    serializer_class = PleasantHabitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Возвращает только привычки текущего пользователя.
        """
        return PleasantHabit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Устанавливаем текущего пользователя как владельца создаваемой привычки.
        """
        serializer.save(user=self.request.user)


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
