from rest_framework.response import Response
from rest_framework import status

from social_network.friends.exceptions import AlreadyExistsError, AlreadyFriendsError
from social_network.users.models import User
from django.db.models import Q

def check_and_prepare_response(func):
    def wrapper(*args, **kwargs):
        response = {
            "data": [],
            "message": "",
            "success": False,
        }
        if kwargs.get("friend"):
            try:
                data, success, message = func(*args, **kwargs)

                response['message'] = message
                if success:
                    response['data'] = data
                    response['success'] = success
                    return Response(response, status=status.HTTP_200_OK)
            except User.DoesNotExist as e:
                response['message'] = "User Does Not Exist."
            except AlreadyExistsError as e:
                response['message'] = e.message
            except AlreadyFriendsError as e:
                response['message'] = e.message
            except Exception as e:
                response['message'] = f"Something Went Wrong. We are Looking into it. - {str(e)}"
        else:
            response['message'] = "Friend name contains null value."
        
        return Response(response, status=status.HTTP_206_PARTIAL_CONTENT)

    return wrapper

def search_user(sent_request, curr_user, search_key):
    if search_key:
        if "@" in search_key:
            users = User.objects.filter(email=search_key).exclude(id__in=sent_request).exclude(
            id=curr_user.id)
        else:
            users = User.objects.filter(Q(username__icontains=search_key)).exclude(id__in=sent_request).exclude(
            id=curr_user.id)
    else:
        users = User.objects.filter.exclude(id__in=sent_request).exclude(
            id=curr_user.id)
    return users
    