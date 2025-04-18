from rest_framework import serializers
from django.contrib.auth import authenticate , get_user_model
from Products.models import Reviews

User = get_user_model()
 
class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    class Meta :
        model = User
        fields = [
            'first_name','last_name','username','email','password' ,'password1' , 'phone_number','birth_date'
        ]


    def validate(self, data):
        if data['password'] != data['password1'] :
            raise serializers.ValidationError({"error":"password didn't match ."})
        
        if User.objects.filter(email=data['email']).exists() :
            raise serializers.ValidationError({"error":"email is already registered ."})
        
        return data


    def create (self , validated_data):
        validated_data.pop('password1')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user




# {
#    "username": "customer1",
#    "email": "customer1@gmail.com",
#    "password": "customer1",
#    "password1": "customer1",
#    "phone_number": "+989123456789"
# }


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        

        user = User.objects.filter(email=email).first()
        if user is None or not user.check_password(password):
            raise serializers.ValidationError("invalid email or password")

        data['user'] = user
        return data
    


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = [
            'username' , 'email' , 'first_name' , 'last_name' , 'phone_number' , 'birth_date' , 'created_at'
        ]
        read_only_fields = ['username' , 'email' , 'created_at']





class UserReviewsSerializer(serializers.ModelSerializer):
    class Meta :
        model = Reviews
        fields = []
        