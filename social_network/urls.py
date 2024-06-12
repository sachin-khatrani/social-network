from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('user/', include('social_network.users.urls')),
    path('', include('social_network.friends.urls')), 
]