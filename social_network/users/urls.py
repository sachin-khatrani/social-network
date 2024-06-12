from django.urls import path
from .views import RegisterAPIView, LoginAPIView, LogoutAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view({"post": "user_register"}), name='register'),
    path('login/', LoginAPIView.as_view({"post": "user_login"}), name='login'),
    path('logout/', LogoutAPIView.as_view({"post": "user_logout"}), name='logout'),
]