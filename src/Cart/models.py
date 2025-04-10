from django.db import models
from Customers.models import Customers
# Create your models here.


# class Carts (models.Model):
#     customer_id = models.ForeignKey(Customers , on_delete=models.CASCADE)
#     # status = 
#     pass



# class CartDetails(models.Model):
#     pass

class Orders(models.Model):

    CHOICE_FIELDS = [
        ('cancelled' , 'cancelled'),
        ('pending' , 'pending'),
        ('processing' , 'processing'),
        ('shipped' , 'shipped'),
        ('delivered' , 'delivered'),
    ]

    # address , product
    customer_id = models.ForeignKey(Customers , on_delete=models.CASCADE)
    # product_id = models.ForeignKey()
    # address_id = models.ForeignKey()
    status = models.CharField(max_length=15 , choices=CHOICE_FIELDS )
    total_price = models.DecimalField(max_digits=5 , decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    discount_price = models.DecimalField(max_digits=2 , decimal_places=2)


class OrderDetail (models.Model):
    pass