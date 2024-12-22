from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "tg_chat_id"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Скрываем пароль, если пользователь не администратор
        request = self.context.get("request")
        if not request or not request.user.is_staff:
            representation.pop("password", None)
        return representation


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            # Проверяем, существует ли пользователь с данным email
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "Пользователь с таким email не существует"
            )

        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed("Неверный email или пароль")

        return super().validate(attrs)
