from rest_framework import serializers
from .models import Orders , OrderDetail



class UserOrderSerializer (serializers.ModelSerializer):
    """
        serializer for user orders. user can change status to 'canclled'
    """
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


class UserOrderDetailSerializer (serializers.ModelSerializer):
    """
        user can see order detail
    """
    product_name = serializers.CharField(source='product.name')

    class Meta :
        model = OrderDetail
        fields = ['product_name','order','single_price','quantity']


class VendorOrderSerializer (serializers.ModelSerializer):
    """
        serializer for vendors. vendors can see shop order and change status for orders
    """
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