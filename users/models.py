from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from habits.models import UsefulHabit, PleasantHabit,  Reward


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет пользователя с указанным email и паролем.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет суперпользователя с указанным email и паролем.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = (
        []
    )
    objects = CustomUserManager()

    def __str__(self):
        return self.email
