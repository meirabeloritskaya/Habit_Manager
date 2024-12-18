from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from habits.serializers import (
    RegisterSerializer,
    UserSerializer,
    TokenSerializer,
    PleasantHabitSerializer,
    RewardSerializer,
)
from rest_framework import viewsets
from habits.models import UsefulHabit, PleasantHabit, Reward
from habits.serializers import HabitSerializer


# Вьюха для регистрации пользователя
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Создаем пользователя
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsefulHabitViewSet(viewsets.ModelViewSet):

    serializer_class = HabitSerializer  # Сериализатор для полезных привычек
    permission_classes = [
        permissions.IsAuthenticated
    ]  # Только для авторизованных пользователей

    def get_queryset(self):
        # Возвращаем только привычки текущего пользователя
        return UsefulHabit.objects.filter(user=self.request.user)


# Вьюха для получения токенов
class TokenObtainView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            refresh = RefreshToken.for_user(request.user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PleasantHabitViewSet(viewsets.ModelViewSet):

    serializer_class = PleasantHabitSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]  # Только для авторизованных пользователей

    def get_queryset(self):
        # Возвращаем только привычки текущего пользователя
        return PleasantHabit.objects.filter(user=self.request.user)


class RewardViewSet(viewsets.ModelViewSet):

    serializer_class = RewardSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]  # Только для авторизованных пользователей

    def get_queryset(self):
        # Возвращаем только вознаграждения текущего пользователя
        return Reward.objects.filter(user=self.request.user)
