from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from core.models import Order, Stock


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=6)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(min_length=6)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            return user

        raise serializers.ValidationError({'detail': 'Could not login with the supplied credentials'})


class StockSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50, allow_blank=False)
    price = serializers.DecimalField(max_digits=8, decimal_places=2, allow_null=False)

    class Meta:
        model = Stock
        fields = ['id', 'name', 'price']


class OrderSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True) 
    stock = serializers.PrimaryKeyRelatedField(queryset=Stock.objects.all(), required=True) 
    type = serializers.ChoiceField(
            choices=[
                (1, 'BUY'),
                (2, 'SELL'),
            ],
            allow_blank=False,
            allow_null=False
        )
    quantity = serializers.IntegerField(min_value=0)

    class Meta:
        model = Order 
        fields = ['id', 'owner', 'stock', 'type', 'quantity']

class TotalInvestedSerializer(serializers.Serializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True) 
    stock = serializers.PrimaryKeyRelatedField(queryset=Stock.objects.all(), required=True)
    total_invested = serializers.SerializerMethodField()

    def get_total_invested(self, data):
        total_stock = data['stock'].get_total_invested(data['owner'])
        return total_stock
