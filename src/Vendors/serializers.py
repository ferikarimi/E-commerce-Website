from rest_framework import serializers
from Vendors.models import  Vendors , VendorCode , Shop
from Accounts.models import User
from phonenumber_field.serializerfields import PhoneNumberField
from django.shortcuts import get_object_or_404
from Products.models import Shop,Product,Comments , Rating
import jdatetime



class VendorRegisterSerializer(serializers.ModelSerializer):
    """
        serializer for register a vendor and create a shop for vendor
    """
    vendor_code = serializers.IntegerField(write_only=True)
    shop_name = serializers.CharField(write_only=True)
    shop_address = serializers.CharField(write_only=True)
    shop_field = serializers.CharField(write_only=True)

    class Meta:
        model = Vendors
        fields =['vendor_code','shop_name','shop_address','shop_field']

    def validate_vendor_code (self , value):
        code_obj = get_object_or_404(VendorCode , code=value , is_used=False)
        self.context['vendor_code_obj'] = code_obj
        return value
    
    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated :
            raise serializers.ValidationError('first register and login then register a shop !')

        user = request.user
        code_obj = self.context['vendor_code_obj']
        if Vendors.objects.filter(vendor_code=code_obj).exists():
            raise serializers.ValidationError('this code is used!')

        shop_name = validated_data.pop('shop_name')
        shop_address = validated_data.pop('shop_address')
        shop_field = validated_data.pop('shop_field')

        vendor = Vendors.objects.create(
            phone=user.phone,
            user=user,
            vendor_code=code_obj,
            role='owner',
        )
        if not user.phone:
            raise serializers.ValidationError('Phone number is required. Please complete your profile first.')

        Shop.objects.create(
            vendor=vendor,
            name=shop_name,
            address=shop_address,
            # phone = user.phone,
            field = shop_field ,
        )
    
        code_obj.is_used = True
        code_obj.save()
        user.is_vendor = True
        user.is_customer = False
        user.save()
        return vendor


class VendorShopSerializer(serializers.ModelSerializer):
    """
        serializer for get shop and update shop detail 
    """
    created_at_shamsi = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()

    class Meta :
        model = Shop
        fields = ['name','address','phone','description' ,'created_at_shamsi']

    def get_phone (self , obj):
        if obj.vendor :
            return str(obj.vendor.phone)
        return None


    def get_created_at_shamsi (self , obj):
        if obj.created_at :
            created_at = obj.created_at
            jalili_data = jdatetime.datetime.fromgregorian(datetime=created_at)
            return jalili_data.strftime('%Y/%m/%d')
        return None


class VendorCodeSerializer(serializers.ModelSerializer):
    """
        serializer for add vendor code. admin caan see and create a code for register vendor
    """
    created_at_shamsi = serializers.SerializerMethodField()

    class Meta :
        model = VendorCode
        fields = ['code','is_used','created_at','created_at_shamsi']

    def get_created_at_shamsi (self , obj):
        if obj.created_at :
            created_at = obj.created_at
            jalili_data = jdatetime.datetime.fromgregorian(datetime=created_at)
            return jalili_data.strftime('%Y/%m/%d')
        return None


class RegisterManagerSerializer (serializers.ModelSerializer):
    """
        serializer for employee 'manager' or 'operator' for vendor shop
    """
    username = serializers.CharField(source='user.username')
    # phone = serializers.CharField(source='user.phone')
    role = serializers.ChoiceField(choices=[('manager', 'manager'), ('operator', 'operator')])

    class Meta :
        model = Vendors
        fields =['username','role']
    
    def create (self , validated_data):
        user_data = validated_data.pop('user')
        username = user_data['username']
        role = validated_data.pop('role')
        # phone = validated_data.pop('phone')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({'username': 'کاربری با این نام پیدا نشد.'})
    
        if Vendors.objects.filter(user=user).exists():
            raise serializers.ValidationError({'user': 'این کاربر قبلاً فروشنده شده.'})
        
        user.is_vendor = True
        user.is_customer = False
        user.save()
        owner_vendor = self.context['request'].user.vendors
        phone = user.phone 
        vendor = Vendors.objects.create(
            user=user ,
            role=role ,
            parent =owner_vendor ,
            phone=phone,
            )
        return vendor


class AllShopSerializer(serializers.ModelSerializer):
    """
        serializer for show all shop and get count product for shops. with jalili date
    """
    created_at_shamsi = serializers.SerializerMethodField()
    product_count = serializers.SerializerMethodField()
    phone = serializers.CharField(source='vendor.phone' , read_only=True)

    class Meta :
        model = Shop
        fields = ['id','name','address','phone','description','field','created_at','product_sold_count' , 'created_at_shamsi' , 'product_count']

    def get_created_at_shamsi (self , obj):
        if obj.created_at :
            created_at = obj.created_at
            jalili_data = jdatetime.datetime.fromgregorian(datetime=created_at)
            return jalili_data.strftime('%Y/%m/%d')
        return None
    
    def get_product_count (self , obj):
        product_count = 0
        products = Product.objects.filter(store_name=obj.id)
        for product in products :
            product_count += product.stock
        return product_count


class ShowOneShopProductsSerializer (serializers.ModelSerializer):
    """
        serializer for show all product af one shop
    """
    class Meta :
        model = Product
        fields = ['category','name','description','price','stock','image','id','final_price' ,'average_rating' , 'store_name']
        read_only_fields = ['category','name','description','price','stock','image','id','final_price','average_rating','store_name']


class SingleShopSerializer (serializers.ModelSerializer):
    """
        serializer for show shop detail
    """
    phone = serializers.CharField(source='vendor.phone' , read_only=True)

    class Meta :
        model = Shop
        fields = ['name','address','phone','description','field']


class ManageCommentsSerializer (serializers.ModelSerializer):
    """
        serializer for manage comments
    """
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)
    customer_username = serializers.CharField(source='customer.username', read_only=True)

    class Meta:
        model = Comments
        fields = ['id','product','comment','status','product_name','product_image','customer_username']