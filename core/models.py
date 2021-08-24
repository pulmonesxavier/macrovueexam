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


