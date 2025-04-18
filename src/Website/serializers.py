from rest_framework import serializers
from Products.models import Product , Discount

class ProductSerializer(serializers.ModelSerializer):

    class Meta :
        model = Product
        fields = [
            'id','name','price','final_price','rating','sold_count','stock','category','vendor','discount'
        ]

    def get_final_price(self , object):
        return object.final_price()
    
    def get_discount(self , object):
        discount = object.discount_set.first()
        if discount :
            return {
                "amount": discount.amount ,
                "is_percentage": discount.is_percentage
            }
        return None