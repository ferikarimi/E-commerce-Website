from rest_framework import serializers
from django.contrib.auth import get_user_model
import jdatetime


User = get_user_model()
class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    class Meta :
        model = User
        fields = ['username','email','password' ,'password1' , 'phone']

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


class UserProfileSerializer(serializers.ModelSerializer):
    created_at_shamsi = serializers.SerializerMethodField()
    class Meta :
        model = User
        fields = [
            'username' , 'email' , 'first_name' , 'last_name' , 'phone' , 'birth_date' , 'created_at' , 'created_at_shamsi'
        ]
        read_only_fields = ['username' , 'email' , 'created_at' , 'created_at_shamsi']

    def get_created_at_shamsi (self , obj):
        if obj.created_at :
            created_at = obj.created_at
            jalili_data = jdatetime.datetime.fromgregorian(datetime=created_at)
            return jalili_data.strftime('%Y/%m/%d - %H:%M:%S')
        return None