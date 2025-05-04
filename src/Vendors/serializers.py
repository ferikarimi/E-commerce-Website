from rest_framework import serializers
from Vendors.models import  Vendors , VendorCode , Shop
from Accounts.models import User
from phonenumber_field.serializerfields import PhoneNumberField
from django.shortcuts import get_object_or_404
from Products.models import Shop,Product
import jdatetime



class VendorRegisterSerializer(serializers.ModelSerializer):
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

        print("Creating Vendor...")
        vendor = Vendors.objects.create(
            phone=user.phone,
            user=user,
            vendor_code=code_obj,
            role='owner',
        )
        print("Vendor created")
        print("Creating shop...")
        if not user.phone:
            raise serializers.ValidationError('Phone number is required. Please complete your profile first.')

        Shop.objects.create(
            vendor=vendor,
            name=shop_name,
            address=shop_address,
            # phone = user.phone,
            field = shop_field ,
        )
        print("Shop created")
    
        code_obj.is_used = True
        code_obj.save()
        user.is_vendor = True
        user.is_customer = False
        user.save()
        return vendor


class VendorProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    phone = PhoneNumberField(source='user.phone', read_only=True)
    birth_date = serializers.CharField(source='user.birth_date')
    created_at_shamsi = serializers.SerializerMethodField()

    class Meta:
        model = Vendors
        fields = [
            'first_name' , 'last_name','username','email','role' , 'phone' ,'birth_date','created_at' , 'created_at_shamsi'
        ]
        read_only_fields = ['username' , 'email' ,'role' , 'created_at' ,'phone' , 'created_at_shamsi' ]

    def get_created_at_shamsi (self , obj):
        if obj.created_at :
            created_at = obj.created_at
            jalili_data = jdatetime.datetime.fromgregorian(datetime=created_at)
            return jalili_data.strftime('%Y/%m/%d - %H:%M:%S')
        return None

    def update (self , instance , validated_data):
        user_data = validated_data.pop('user',{})

        for attr , value in validated_data.items():
            setattr(instance , attr , value)
        instance.save()

        user = instance.user
        if 'first_name' in user_data :
            user.first_name = user_data['first_name']

        if 'last_name' in user_data :
            user.last_name = user_data['last_name']
        user.save()
        return instance


class VendorShopSerializer(serializers.ModelSerializer):
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
    created_at_shamsi = serializers.SerializerMethodField()

    class Meta :
        model = VendorCode
        fields = ['code','is_used','created_at' , 'created_at_shamsi']

    def get_created_at_shamsi (self , obj):
        if obj.created_at :
            created_at = obj.created_at
            jalili_data = jdatetime.datetime.fromgregorian(datetime=created_at)
            return jalili_data.strftime('%Y/%m/%d')
        return None


class RegisterManagerSerializer (serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=[('manager', 'manager'), ('operator', 'operator')])

    class Meta :
        model = Vendors
        fields =['username','role']
    
    def create (self , validated_data):
        username = validated_data.pop('username')
        role = validated_data.pop('role')

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
        vendor = Vendors.objects.create(
            user=user ,
            role=role ,
            parent =owner_vendor ,
            )
        return vendor


class ManagerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    created_at_shamsi = serializers.SerializerMethodField()

    class Meta:
        model = Vendors
        fields = ['username', 'role', 'created_at' , 'created_at_shamsi']

    def get_created_at_shamsi (self , obj):
        if obj.created_at :
            created_at = obj.created_at
            jalili_data = jdatetime.datetime.fromgregorian(datetime=created_at)
            return jalili_data.strftime('%Y/%m/%d')
        return None


class AllShopSerializer(serializers.ModelSerializer):
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


class SingleShopSerializer (serializers.ModelSerializer):
    class Meta :
        model = Shop
        fields = ['name','address','phone','description','field']


class ShowOneShopProductsSerializer (serializers.ModelSerializer):
    class Meta :
        model = Product
        fields = ['category','name','description','price','stock','image','id','final_price' ,'rating' , 'store_name']
        read_only_fields = ['category','name','description','price','stock','image','id','final_price','rating','store_name']