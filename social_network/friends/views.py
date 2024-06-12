from django.http import JsonResponse
from django.shortcuts import render
from social_network.friends.exceptions import AlreadyExistsError, AlreadyFriendsError
from django.core.exceptions import ObjectDoesNotExist

from social_network.friends.serializer import FriendshipRequestSerializer
from social_network.friends.utils import check_and_prepare_response, search_user

# Create your views here.
from .models import Friend, FriendshipRequest
from social_network.users.models import User
from social_network.users.serializers import UserListSerializer
from django.db.models import Q

from rest_framework.mixins import ListModelMixin
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle


class FriendsListView(viewsets.GenericViewSet, ListModelMixin):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_users(self, request):
        """
        Get all users which are not friends and not pending request
        """ 
        search_key = request.query_params.get("search")
        sent_request = list(
            FriendshipRequest.objects.filter(Q(from_user=request.user))
            .exclude(to_user_id=request.user.id)
            .values_list('to_user_id', flat=True))
        
        users = search_user(sent_request, request.user, search_key)

        paginated_queryset = self.paginate_queryset(users)
        return Response({"data": UserListSerializer(paginated_queryset, many=True).data, "success": True}, status=status.HTTP_201_CREATED)
    
    def get_pending_requests(self, request):
        """
        Get all pending friend requests received by the current user.
        """
        pen_request =  FriendshipRequest.objects.get_friend_requests(user=request.user)

        paginated_queryset = self.paginate_queryset(pen_request)
        return Response({"data": FriendshipRequestSerializer(paginated_queryset, many=True).data, "success": True}, status=status.HTTP_200_OK)
    
    def get_friends(self, request):
        """
        Get all friends of the current user.
        """
        friends_obj = list(Friend.objects.select_related("from_user", "to_user").filter(to_user=request.user).all())

        paginated_queryset = self.paginate_queryset(friends_obj)
        friends = [UserListSerializer(frd.from_user).data for frd in paginated_queryset]
        return Response({"data": friends, "success": True}, status=status.HTTP_200_OK)
    
class FriendsShipActionView(viewsets.GenericViewSet):
    """
    View to handle friend-related actions such as sending, accepting, rejecting, and canceling friend requests.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    @check_and_prepare_response
    def send_request(self, request, friend=None):
        """
        Send a friend request to the specified user.
        """
        friend_user = User.objects.get(username=friend)
            
        friend_request = FriendshipRequest.objects.add_friend(request.user, friend_user, message='Hi! I would like to add you')
        return FriendshipRequestSerializer(friend_request).data, True, "Friend Request Send Successfully."
    
    @check_and_prepare_response
    def accept_request(self, request, friend=None):
        """
        Accept a friend request from the specified user.
        """
        friend_user = User.objects.get(username=friend)

        try:
            friend_request = FriendshipRequest.objects.get(to_user=request.user, from_user=friend_user)
        
            res = friend_request.accept()
            if res:
                return [], True, "Friend Request Accepted"
            else:
                return [], False, "Error to Accept Friend Request"
        except ObjectDoesNotExist:
            return [], False, "Pending Request Not Found From this user"


    @check_and_prepare_response
    def reject_request(self, request, friend=None):
        """
        Reject a friend request from the specified user.
        """
        friend_user = User.objects.get(username=friend)
        
        try:
            friend_request = FriendshipRequest.objects.get(to_user=request.user, from_user=friend_user)
            res = friend_request.reject()

            if res:
                return [], True, "Friend Request Rejected"
            else:
                return [], False, "Error to Reject Friend Request"
        except ObjectDoesNotExist:
            return [], False, "Pending Request Not Found From this user"
    
    @check_and_prepare_response
    def cancel_request(self, request, friend=None):
        """
        Cancel a friend request sent to the specified user.
        """
        try:
            friend_user = User.objects.get(username=friend)
            friend_request = FriendshipRequest.objects.get(from_user=request.user, to_user=friend_user, status="pending")
            res = friend_request.cancel()

            if res:
                return [], True, "Friend Request Cancelled"
            else:
                return [], False, "Error to Cancel Friend Request"
        except ObjectDoesNotExist:
            return [], False, "Pending Request Not Found From this user"