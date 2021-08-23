from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from core.serializer import UserSerializer 

from rest_framework import status, permissions, viewsets
from rest_framework.response import Response


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

