from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer, TokenSerializer
from rest_framework import viewsets
from .models import UsefulHabit
from .serializers import HabitSerializer


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
    queryset = UsefulHabit.objects.all()  # Здесь выбираем все полезные привычки
    serializer_class = HabitSerializer  # Сериализатор для полезных привычек
    permission_classes = [permissions.IsAuthenticated]  # Только для авторизованных пользователей

    def perform_create(self, serializer):
        # Здесь связываем полезную привычку с текущим пользователем
        serializer.save(user=self.request.user)


# Вьюха для получения токенов
class TokenObtainView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            refresh = RefreshToken.for_user(request.user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
