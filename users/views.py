from rest_framework import status, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.exceptions import PermissionDenied

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для управления пользователями (CRUD).
    Только администраторы могут видеть список пользователей"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("Доступ разрешен только администраторам.")
        return super().list(request, *args, **kwargs)


class UserCreateAPIView(CreateAPIView):
    """Эндпоинт для регистрации новых пользователей"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class CustomTokenObtainPairView(TokenObtainPairView):
    """Кастомный класс для получения токена"""

    serializer_class = CustomTokenObtainPairSerializer
