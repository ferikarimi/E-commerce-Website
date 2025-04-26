from django.db import models
from Accounts.models import User


class Addresses (models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE, related_name='addresses')
    city = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return f"address : {self.city} : {self.address}"