from rest_framework import serializers
from .models import Product , Reviews


class ReviewsSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name' , read_only=True)
    product_image = serializers.ImageField(source='product.image' , read_only=True)

    class Meta :
        model = Reviews
        fields = '__all__'


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