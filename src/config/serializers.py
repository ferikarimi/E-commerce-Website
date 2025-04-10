from rest_framework import serializers
from Accounts.models import Customers
from Vendors.models import  Vendors , VendorCode , Shop
from django.contrib.auth import authenticate , get_user_model
# from users_app.models import Con


class CustomerRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    class Meta :
        model = Customers
        fields = [
            'first_name','last_name','username','email','password' ,'password1' , 'phone_number','birth_date'
        ]


    def validate(self, data):
        if data['password'] != data['password1'] :
            raise serializers.ValidationError({"error":"password didn't matc ."})
        
        if Customers.objects.filter(email=data['email']).exists() :
            raise serializers.ValidationError({"error":"email is already registered ."})
        
        if Customers.objects.filter(username=data['username']).exists() :
            raise serializers.ValidationError({"error":"username is already taken."})
        
        return data


    def create (self , validated_data):
        validated_data.pop('password1')
        password = validated_data.pop('password')
        user = Customers(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):

    class Meta :
        model = Customers
        fields = ['email' , 'password']

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = Customers.objects.filter(email=email).first()
        if user is None or not user.check_password(password):
            raise serializers.ValidationError("invalid email or password")

        data['user'] = user
        return data
    


User = get_user_model()

class VendorRegisterSerializer(serializers.ModelSerializer):
    vendor_code = serializers.IntegerField(write_only=True)
    shop_name = serializers.CharField(write_only=True)
    shop_address = serializers.CharField(write_only=True)

    class Meta:
        model = Vendors
        fields =['vendor_code','shop_name','shop_address']

    def validate_vendor_code (self , value):
        try :
            code_obj = VendorCode.objects.get(code=value , is_used=False)
        except VendorCode.DoesNotExist :
            raise serializers.ValidationError("can not used this code ! invalid code")
        self.context['vendor_code_obj'] = code_obj
        return value
    

    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated :
            raise serializers.ValidationError('first register and login then register a shop !')

        user = request.user
        code_obj = self.context['vendor_code_obj']
        shop_name = validated_data.pop('shop_name')
        shop_address = validated_data.pop('shop_address')

        vendor = Vendors.objects.create(
            user=user,
            vendor_code=code_obj,
            role='owner',
            is_vendor=True,
            is_customer=False,
        )
        Shop.objects.create(
            vendor=vendor,
            name=shop_name,
            address=shop_address,
            phone = user.phone_number,
            descroption='',
        )
    
        code_obj.is_used = True
        code_obj.save()
        return vendor


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta :
        model = Customers
        fields = [
            'username' , 'email' , 'first_name' , 'last_name' , 'phone_number' , 'birth_date' , 'created_at'
        ]
        read_only_fields = ['username' , 'email' , 'created_at']












# {
#    "username": "customer1",
#    "email": "customer1@gmail.com",
#    "password": "customer1",
#    "password1": "customer1",
#    "phone_number": "+989123456789"
# }