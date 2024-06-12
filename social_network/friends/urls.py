from django.urls import path
from .views import *

app_name = "friends"

urlpatterns = [
    path('find-friends', FriendsListView.as_view({"get":"get_users"}), name="find-friends"),
    path('friend-requests', FriendsListView.as_view({"get": "get_pending_requests"}), name="friend-requests"),
    path('friends', FriendsListView.as_view({"get": "get_friends"}), name="friends"),
    path('send-request/<slug:friend>', FriendsShipActionView.as_view({"post": "send_request"}), name="send-request"),
    path('accept-request/<slug:friend>', FriendsShipActionView.as_view({"post": "accept_request"}), name="accept-request"),
    path('reject-request/<slug:friend>', FriendsShipActionView.as_view({"delete": "reject_request"}), name="reject-request"),
    path('cancel-request/<slug:friend>', FriendsShipActionView.as_view({"delete": "cancel_request"}), name="cancel-request"),
]
