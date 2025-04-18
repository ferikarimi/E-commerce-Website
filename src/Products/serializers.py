from rest_framework import serializers
from .models import Product


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta :
        model = Product
        fileds = '__all__'


class VendorProductSerializer (serializers.ModelSerializer):
    class Meta :
        model = Product
        fields = [
            'category_id','name','description','price','stock','image','id'
        ]

class VendorSetProductSerializer (serializers.ModelSerializer):
    class Meta :
        model = Product
        fields = [
            'name','description' , 'price','stock','rating','store_name' , 'image'
        ]
        read_only_fields =[
            'name','description' , 'price','stock','rating','store_name' , 'image'
        ]



class AllProductSerializer (serializers.ModelSerializer):
    final_price = serializers.SerializerMethodField()

    class Meta :
        model = Product
        fields = [
            'category_id','name','description','price','stock','image','id' , 'final_price'
        ]
    def get_final_price (self , obj):
        return obj.final_price()