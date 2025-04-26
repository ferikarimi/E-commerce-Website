from django.db import models
from Accounts.models import User
from Products.models import Product
from Customers.models import Addresses


class Orders(models.Model):

    CHOICE_FIELDS = [
        ('cancelled' , 'cancelled'),
        ('pending' , 'pending'),
        ('processing' , 'processing'),
        ('shipped' , 'shipped'),
        ('delivered' , 'delivered'),
    ]

    customer = models.ForeignKey(User , on_delete=models.CASCADE)
    address = models.OneToOneField(Addresses , on_delete=models.CASCADE , related_name='order_adddress')
    status = models.CharField(max_length=15 , choices=CHOICE_FIELDS )
    total_price = models.DecimalField(max_digits=5 , decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    discount_price = models.DecimalField(max_digits=2 , decimal_places=2)


class OrderDetail (models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name='items')
    order = models.ForeignKey(Orders , on_delete=models.CASCADE , related_name='order')
    single_price = models.DecimalField(max_digits=5 , decimal_places=2)