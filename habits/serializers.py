from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from habits.models import UsefulHabit, PleasantHabit, Reward
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# Сериализатор для регистрации пользователя
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "first_name", "last_name"]

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        return user


class UsefulSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = UsefulHabit
        fields = "__all__"

    def get_is_owner(self, obj):
        request = self.context.get("request")
        return request.user == obj.user if request else False

    def validate(self, attrs):
        # Проверяем, что reward и related_habit принадлежат тому же пользователю
        reward = attrs.get("reward")
        related_habit = attrs.get("related_habit")
        user = self.context["request"].user

        if reward and reward.user != user:
            raise serializers.ValidationError(
                "Вознаграждение должно принадлежать текущему пользователю."
            )
        if related_habit and related_habit.user != user:
            raise serializers.ValidationError(
                "Связанная привычка должна принадлежать текущему пользователю."
            )
        return attrs


class PleasantHabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = PleasantHabit
        fields = "__all__"


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = "__all__"


# Сериализатор для пользователя
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "email", "first_name", "last_name", "is_active", "is_staff"]
