from django.urls import path, include
from rest_framework.routers import DefaultRouter
from habits.views import UsefulHabitViewSet, PleasantHabitViewSet, RewardViewSet


app_name = "habits"

router = DefaultRouter()
router.register(r"useful_habits", UsefulHabitViewSet, basename="useful_habit")
router.register(r"pleasant_habits", PleasantHabitViewSet, basename="pleasant_habit")
router.register(r"rewards", RewardViewSet, basename="reward")

urlpatterns = [
    path("", include(router.urls)),
]
