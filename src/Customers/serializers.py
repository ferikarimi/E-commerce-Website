from rest_framework import serializers
from Customers.models import Addresses



class AddressSerializer(serializers.ModelSerializer):
    """
        serializer for user addresses
    """
    class Meta :
        model = Addresses
        fields =['id' , 'city' , 'address']

    def create(self, validated_data):
        user = self.context['request'].user
        return Addresses.objects.create(customer=user,**validated_data)