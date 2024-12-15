from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('token/', views.TokenObtainView.as_view(), name='token_obtain'),
]
