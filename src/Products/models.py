from django.db import models
from Vendors.models import Vendors
from Accounts.models import Customers

# Create your models here.



class Category (models.Model):
    name = models.CharField(max_length=30)
    parent_id = models.ForeignKey('self' , on_delete=models.PROTECT)



class Product(models.Model):
    category_id = models.ForeignKey(Category , on_delete=models.CASCADE)
    vendor_id = models.ForeignKey(Vendors , models.CASCADE)
    name = models.CharField(max_length=35)
    description = models.TextField()
    price = models.DecimalField(max_digits=5 , decimal_places=2)
    # image = 
    stock = models.IntegerField()


class Discount(models.Model):
    product_id = models.ForeignKey(Product , on_delete=models.CASCADE)
    vendor_id = models.ForeignKey(Vendors , on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=2 , decimal_places=2)
    discount_code = models.IntegerField(default=None)
    is_percentage = models.BooleanField(default=None)


class Reviews(models.Model):
    RATING_CHOICE_FIELD = {
        ('1' , 1),
        ('2' , 2),
        ('3' , 3),
        ('4' , 4),
        ('5' , 5)
    }
    COMMENT_CHOICE_FIELDS = {
        ('pending', 'pending'),
        ('approved', 'approved') ,
        ('rejected' , 'rejected')
    }
    customer_id = models.ForeignKey(Customers , on_delete=models.CASCADE)
    prudoct_id = models.ForeignKey(Product , on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICE_FIELD , default=None)
    comment = models.TextField()
    status = models.CharField(max_length=8 , default='pending')