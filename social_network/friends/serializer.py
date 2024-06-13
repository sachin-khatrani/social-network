from rest_framework import serializers
from social_network.friends.models import FriendshipRequest
from social_network.users.serializers import UserSerializer

class FriendshipRequestSerializer(serializers.ModelSerializer):
    from_user = UserSerializer()
    to_user = UserSerializer()
    class Meta:
        model = FriendshipRequest
        fields = "__all__"
