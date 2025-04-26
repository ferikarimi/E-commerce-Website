from django.db import models
from Vendors.models import Vendors , Shop
from Accounts.models import User


class Category (models.Model):
    name = models.CharField(max_length=30)
    parent = models.ForeignKey('self' , on_delete=models.PROTECT , null=True , blank=True)


class Product(models.Model):
    category = models.ForeignKey(Category , on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendors , models.CASCADE)
    name = models.CharField(max_length=35)
    description = models.TextField()
    price = models.DecimalField(max_digits=8 , decimal_places=2)
    image = models.ImageField(upload_to='product_images' , null=True , blank=True)
    stock = models.IntegerField()
    rating = models.DecimalField(max_digits=1 , decimal_places=1 , default=0.0)
    sold_count = models.IntegerField(default=0)
    store_name = models.ForeignKey(Shop , on_delete=models.PROTECT , related_name='store_name')
    created_at = models.DateTimeField(auto_now_add=True)


    def final_price(self):
        discount = self.discount_set.first()
        if discount :
            if discount.is_percentage:
                return self.price * (1 - discount.amount / 100)
            else :
                return self.price - discount.amount
        return self.price


class Discount(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendors , on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=2 , decimal_places=2)
    discount_code = models.IntegerField(default=None)
    is_percentage = models.BooleanField(default=True)


class Reviews(models.Model):
    RATING_CHOICE_FIELD = {
        (1 , '1'),
        (2 , '2'),
        (3 , '3'),
        (4 , '4'),
        (5 , '5'),
    }
    STATUS_CHOICE_FIELDS = {
        ('pending', 'pending'),
        ('approved', 'approved') ,
        ('rejected' , 'rejected')
    }
    customer = models.ForeignKey(User , on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICE_FIELD , default=None)
    comment = models.TextField()
    status = models.CharField(max_length=8 , choices=STATUS_CHOICE_FIELDS ,default='pending')