from rest_framework import serializers
from Vendors.models import  Vendors , VendorCode , Shop
from Accounts.models import User
from phonenumber_field.serializerfields import PhoneNumberField
from django.shortcuts import get_object_or_404





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

        vendor = Vendors.objects.create(
            user=user,
            vendor_code=code_obj,
            role='owner',

        )
        Shop.objects.create(
            vendor=vendor,
            name=shop_name,
            address=shop_address,
            phone = user.phone_number,
            field = shop_field ,
        )
    
        code_obj.is_used = True
        code_obj.save()
        return vendor



# {
#    "vendor_code": 1111,
#    "shop_name": "vendor1_shop",
#    "shop_address": "shiraz"
# }


class VendorProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    phone_number = PhoneNumberField(source='user.phone_number', read_only=True)
    birth_date = serializers.CharField(source='user.birth_date')

    class Meta:
        model = Vendors
        fields = [
            'first_name' , 'last_name','username','email','role' , 'phone_number' ,'birth_date','created_at'
        ]
        read_only_fields = ['username' , 'email' ,'role' , 'created_at' ,'phone_number' ]

    
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
    class Meta :
        model = Shop
        fields = [
            'name','address','phone','description'
        ]
















class VendorCodeSerializer(serializers.ModelSerializer):
    class Meta :
        model = VendorCode
        fields = ['code','is_used','created_at']












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

    class Meta:
        model = Vendors
        fields = ['username', 'role', 'created_at']