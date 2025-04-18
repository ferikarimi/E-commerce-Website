from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import AddressSerializer
from Customers.models import Addresses



class GetUserAddresses (APIView):
    def get (self , request):
        addresses = request.user.addresses.all()
        serializer = AddressSerializer(addresses , many=True)
        return Response (serializer.data)


class CreateAddress(APIView):
    def post (self , request):
        city = request.data.get('city')
        address = request.data.get('address')

        if city and address :
            new_address = Addresses.objects.create(
                user = request.user ,
                city = city ,
                address = address
            )
            return Response(AddressSerializer(new_address).data , status=201)
        else :
            return Response ({'error':'city and address are required!'} , status=400)


class UpdateAddress(APIView):
    def put (self , request):
        address_data = request.data.get('addresses',[])
        for addr in address_data :
            try :
                address = request.user.addresses.get(id=addr.get('id'))
                serializer = AddressSerializer (address , data=addr)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else :
                    return Response(serializer.errors , status=400)
            except Addresses.DoesNotExist :
                return Response({'error':'address not found'}, status=404)
        
        return Response(AddressSerializer(request.user.addresses.all() , many=True).data)


class DeleteAddress(APIView):
    def delete (self , request ,id):
        try :
            address = request.user.addresses.get(id=id)
            address.delete()
            return Response({'success':True , 'message':'address deleted !'})
        except Addresses.DoesNotExist :
            return Response({'error':'address not found'}, status=404)      