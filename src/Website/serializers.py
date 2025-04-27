from rest_framework import serializers
from Products.models import Shop,Product

class AllShopSerializer(serializers.ModelSerializer):


    class Meta :
        model = Shop
        fields = ['id','name','address','phone','description','field','created_at','product_sold_count']


class SingleShopSerializer (serializers.ModelSerializer):
    class Meta :
        model = Shop
        fields = ['name','address','phone','description','field']


class ShowOneShopProductsSerializer (serializers.ModelSerializer):
    class Meta :
        model = Product
        fields = [
            'category','name','description','price','stock','image','id','final_price'
            ]
        read_only_fields = [
            'category','name','description','price','stock','image','id','final_price'
            ]