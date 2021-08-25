from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

from rest_framework import permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from core.models import Order, Stock
from core.serializer import LoginSerializer, OrderSerializer, StockSerializer, UserSerializer


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


class StockViewSet(viewsets.ViewSet):
    """
    ViewSet for stocks
    """
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def create(self, request):
        serializer = StockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        if request.GET.get('search'):
            search_param = request.GET.get('search')
            queryset = Stock.objects.filter(name__contains=search_param)
        else:
            queryset = Stock.objects.all()
        serializer = StockSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = Stock.objects.all()
        stock = get_object_or_404(queryset, pk=pk)
        serializer = StockSerializer(stock)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderViewSet(viewsets.ViewSet):
    """
    ViewSet for Orders
    """

    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['owner'] != request.user:
                return Response({'detail': 'Unable to create orders for other users'}, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = Order.objects.filter(owner=request.user)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = Order.objects.filter(owner=request.user)
        order = get_object_or_404(queryset, pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
