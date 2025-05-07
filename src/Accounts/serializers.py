from rest_framework import serializers
import jdatetime
from .models import User



class UserRegisterSerializer(serializers.ModelSerializer):
    """
        serializer for register users and validate password and check email and phone
    """
    password1 = serializers.CharField(write_only=True)
    class Meta :
        model = User
        fields = ['username','email','password' ,'password1' , 'phone']

    def validate(self, data):
        if data['password'] != data['password1'] :
            raise serializers.ValidationError({"error":"password didn't match ."})
        
        if User.objects.filter(email=data['email']).exists() :
            raise serializers.ValidationError({"error":"email is already registered ."})

        if User.objects.filter(phone=data['phone']).exists() :
            raise serializers.ValidationError({"error":"phone is already registered ."})
        
        return data

    def create (self , validated_data):
        validated_data.pop('password1')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user    


class UserProfileSerializer(serializers.ModelSerializer):
    """
        serializer for show and update users profile. validate username and email and phone after update profile
    """
    created_at_shamsi = serializers.SerializerMethodField()
    class Meta :
        model = User
        fields = [
            'username' , 'email' , 'first_name' , 'last_name' , 'phone' , 'birth_date' , 'created_at' , 'created_at_shamsi'
        ]
        read_only_fields = ['created_at' , 'created_at_shamsi']
    
    def validate_username(self, value):
        user = self.instance
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError("این نام کاربری قبلاً ثبت شده است.")
        return value

    def validate_email(self, value):
        user = self.instance
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("این ایمیل قبلاً ثبت شده است.")
        return value

    def validate_phone(self, value):
        user = self.instance
        if User.objects.exclude(pk=user.pk).filter(phone=value).exists():
            raise serializers.ValidationError("این شماره تلفن قبلاً ثبت شده است.")
        return value

    def get_created_at_shamsi (self , obj):
        if obj.created_at :
            created_at = obj.created_at
            jalili_data = jdatetime.datetime.fromgregorian(datetime=created_at)
            return jalili_data.strftime('%Y/%m/%d - %H:%M:%S')
        return None