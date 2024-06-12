from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, UserLoginSerializer, UserLogoutSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets


User = get_user_model()

class RegisterAPIView(viewsets.GenericViewSet):
    def user_register(self, request):
        """
        Register a new user.

        Args:
            request: Request object containing user registration data.

        Returns:
            Response: JSON response with user data if registration is successful,
            or error message if registration fails.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Register User Successfully.","success": True}, status=status.HTTP_201_CREATED)
        return Response({"data": serializer.errors, "success": False}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(viewsets.GenericViewSet):
    def user_login(self, request):
        """
        Log in a user.

        Args:
            request: Request object containing user login credentials.

        Returns:
            Response: JSON response with access and refresh tokens if login is successful,
            or error message if login fails.
        """
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({"data": {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, "success": True}, status=status.HTTP_200_OK)
        return Response({"data": [], "success": False,'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutAPIView(viewsets.GenericViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def user_logout(self, request):
        """
        Log out a user.

        Args:
            request: Request object containing user data.

        Returns:
            Response: JSON response indicating successful logout,
            or error message if logout fails.
        """
        serializer = UserLogoutSerializer(data=request.data)
        if serializer.is_valid():
            response = Response({"data":[], "success": True, 'message': 'Logout successful'}, status=status.HTTP_200_OK)
            response.delete_cookie('jwt_token')  #
            return response
        return Response({"data": [], "success": False,'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
