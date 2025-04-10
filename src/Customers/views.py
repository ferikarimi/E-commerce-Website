from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import AddressSerializer
from Customers.models import Addresses


@api_view(['GET'])
def get_addresses(request):
    addresses = request.user.addresses.all()
    serializer = AddressSerializer(addresses , many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_address(request):

    serializer = AddressSerializer(data=request.data , context={'request':request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data , status=status.HTTP_201_CREATED)
    return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_addresses(request):

    addresses_data = request.data.get('addresses',[])
    
    for addr in addresses_data :
        try:
            address = request.user.addresses.get(id=addr.get('id'))
            serializer = AddressSerializer(address , data=addr)
            if serializer.is_valid():
                serializer.save()
            else :
                return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        except Addresses.DoesNotExist :
            return Response({'error':'address not found'}, status=status.HTTP_404_NOT_FOUND)
        
    return Response(AddressSerializer(request.user.addresses.all() , many=True).data)


@api_view(['DELETE'])
def delete_addresses(request):
    try:
        address = request.user.addresses.get(id=request.data.get('id'))
        address.delete()
        return Response({'message':'address deleted !'})
    except Addresses.DoesNotExist :
        return Response({'error':'address not found'}, status=status.HTTP_404_NOT_FOUND)