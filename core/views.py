from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

from rest_framework import status, permissions, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from core.serializer import UserSerializer, LoginSerializer


class SignUpViewSet(viewsets.ViewSet):
    """
    ViewSet for creating a user
    """
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginViewSet(viewsets.ViewSet):
    """
    ViewSet for logging in
    """
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutViewSet(viewsets.ViewSet):
    """
    ViewSet for logging out
    """

    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        logout(request)
        return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)
