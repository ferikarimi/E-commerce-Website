from rest_framework import serializers
from Products.models import Shop,Product
import jdatetime

class AllShopSerializer(serializers.ModelSerializer):
    created_at_shamsi = serializers.SerializerMethodField()



    class Meta :
        model = Shop
        fields = ['id','name','address','phone','description','field','created_at','product_sold_count' , 'created_at_shamsi']

    def get_created_at_shamsi (self , obj):
        if obj.created_at :
            created_at = obj.created_at
            jalili_data = jdatetime.datetime.fromgregorian(datetime=created_at)
            return jalili_data.strftime('%Y/%m/%d - %H:%M:%S')
        return None

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