from rest_framework import serializers
from .models import Orders , OrderDetail
# from .models import 



class UserOrderSerializer (serializers.ModelSerializer):
    address = serializers.SerializerMethodField()

    class Meta :
        model = Orders
        fields = ['id','customer','address','status','total_price','order_date','discount_price']
        read_only_fields = ['id','customer','address','total_price','order_date','discount_price']

    def validate_status(self, value):
        instance = self.instance
        if instance and value != 'cancelled':
            raise serializers.ValidationError ('you just can cancelled an order !')
        return value
    
    def get_address(self, obj):
        return str(obj.address)
        

class VendorOrderSerializer (serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()


    class Meta :
        model = Orders
        fields = ['id','customer','address','status','total_price','order_date','discount_price']
        read_only_fields = ['id','customer','address','total_price','order_date','discount_price']
        
    def get_address(self, obj):
        return str(obj.address)
        
    def get_customer(self , obj):
        return str(obj.customer.username)
    


# class OrderDetailSerializer(serializers.ModelSerializer):
#     class Meta :
#         model = OrderDetail
#         fields = ['product','single_price','quantity']

