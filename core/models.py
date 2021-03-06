from django.contrib.auth.models import User
from django.db import models


class Stock(models.Model):
    """
    Stock model that holds the necessary information for a specific stock
    """
    name = models.CharField(max_length=50, blank=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name

    def get_total_invested(self, user):
        
        total_invested = 0
        order_list = Order.objects.filter(owner=user, stock=self)
        for order in order_list:
            total_invested += (float(order.quantity)*float(self.price))
        return total_invested


class Order(models.Model):
    """
    Order model that summarizes information on user orders
    """
    TYPE_CHOICES = [
        (1, 'BUY'),
        (2, 'SELL'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    type = models.IntegerField(choices=TYPE_CHOICES, blank=False) 
    quantity = models.PositiveIntegerField(default=0)

