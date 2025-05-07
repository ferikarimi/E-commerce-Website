from django.db import models
from Vendors.models import Vendors , Shop
from Accounts.models import User
from django.core.validators import MinValueValidator , MaxValueValidator



class Category (models.Model):
    class Meta:
        verbose_name_plural = "Categories | دسته بندی‌ها"

    name = models.CharField(max_length=30)
    parent = models.ForeignKey('self' , on_delete=models.PROTECT , null=True , blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    class Meta:
        verbose_name_plural = "Products | محصولات"

    category = models.ForeignKey(Category , on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendors , models.CASCADE)
    name = models.CharField(max_length=35)
    description = models.TextField()
    price = models.DecimalField(max_digits=8 , decimal_places=2)
    image = models.ImageField(upload_to='product_images' , null=True , blank=True)
    stock = models.IntegerField()
    # rating = models.DecimalField(max_digits=2 , decimal_places=1 , default=0.0 , validators=[MinValueValidator(0.0) , MaxValueValidator(5.0)])
    average_rating = models.FloatField(default=None , null=True, blank=True)

    sold_count = models.IntegerField(default=0)
    store_name = models.ForeignKey(Shop , on_delete=models.PROTECT , related_name='product')
    created_at = models.DateTimeField(auto_now_add=True)

    def final_price(self):
        discount = self.discount.first()
        if discount :
            if discount.is_percentage:
                return self.price * (1 - discount.amount / 100)
            else :
                return self.price - discount.amount
        return self.price
    
    def __str__(self):
        return self.name


class Discount(models.Model):
    class Meta:
        verbose_name_plural = "Discounts | تخفیف‌ها"

    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name='discount')
    amount = models.DecimalField(max_digits=6 , decimal_places=2)
    discount_code = models.IntegerField(default=None , null=True , blank=True)
    is_percentage = models.BooleanField(default=True)


class Comments(models.Model):
    class Meta:
        verbose_name_plural = "Comments | نظرات"

    STATUS_CHOICE_FIELDS = [
        ('pending', 'pending'),
        ('approved', 'approved') ,
        ('rejected' , 'rejected')
    ]
    customer = models.ForeignKey(User , on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name='product_comments')
    comment = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=8 , choices=STATUS_CHOICE_FIELDS ,default='pending')
    created_at = models.DateTimeField(auto_now_add=True)


class Rating(models.Model):
    class Meta:
        verbose_name_plural = "Rating | امتیازها"

    RATING_CHOICE_FIELD = [
        (1 , '1'),
        (2 , '2'),
        (3 , '3'),
        (4 , '4'),
        (5 , '5'),
    ]
    customer = models.ForeignKey(User , on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name='product_rating')
    rating = models.IntegerField(choices=RATING_CHOICE_FIELD , default=None , null=True, blank=True)