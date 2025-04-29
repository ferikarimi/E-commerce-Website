from django.db import models
from Accounts.models import User
from Products.models import Product
from Customers.models import Addresses


class Orders(models.Model):
    class Meta:
        verbose_name_plural = "Orders | سفارش‌ها"

    CHOICE_FIELDS = [
        ('cancelled' , 'cancelled'),
        ('pending' , 'pending'),
        ('processing' , 'processing'),
        ('shipped' , 'shipped'),
        ('delivered' , 'delivered'),
    ]

    customer = models.ForeignKey(User , on_delete=models.CASCADE)
    address = models.ForeignKey(Addresses , on_delete=models.CASCADE , related_name='order_adddress')
    status = models.CharField(max_length=15 , choices=CHOICE_FIELDS )
    total_price = models.DecimalField(max_digits=8 , decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    discount_price = models.DecimalField(max_digits=8 , decimal_places=2 , null=True , blank=True)


class OrderDetail (models.Model):
    class Meta:
        verbose_name_plural = "OrderDetail | جزئیات سفارش‌ها"

    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name='items')
    order = models.ForeignKey(Orders , on_delete=models.CASCADE , related_name='order')
    single_price = models.DecimalField(max_digits=8 , decimal_places=2 , null=True , blank=True)
    quantity = models.PositiveIntegerField(default=1)