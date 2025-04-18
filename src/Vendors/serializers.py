from rest_framework import serializers
from Vendors.models import  Vendors , VendorCode , Shop
# from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.serializerfields import PhoneNumberField




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
        if Vendors.objects.filter(vendor_code=code_obj).exists():
            raise serializers.ValidationError('this code is used!')
        
        shop_name = validated_data.pop('shop_name')
        shop_address = validated_data.pop('shop_address')

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
            'first_name' , 'last_name','username','email','role' , 'phone_number' ,'birth_date','created_at' , 'is_customer' , 'is_vendor'
        ]
        read_only_fields = ['username' , 'email' ,'role' , 'created_at' , 'is_customer' ,'phone_number' , 'is_vendor']

    
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






















class VendorRoleSerializer(serializers.ModelSerializer):
    pass

