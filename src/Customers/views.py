from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AddressSerializer
from Customers.models import Addresses
from rest_framework.permissions import IsAuthenticated



class GetUserAddresses (APIView):
    """
        get, create, update and delete user`s addresses
    """
    permission_classes = [IsAuthenticated]
    
    def get (self , request):
        addresses = request.user.addresses.all()
        serializer = AddressSerializer(addresses , many=True)
        return Response (serializer.data , status=200)
    
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

    def put (self , request , id):
        try :
            address = request.user.addresses.get(id=id)
            serializer = AddressSerializer(address , data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data , status=200)
            return Response(serializer.errors , status=400)
        except Addresses.DoesNotExist :
            return Response({'error':'address not found'}, status=404)

    def delete (self , request ,id):
        try :
            address = request.user.addresses.get(id=id)
            address.delete()
            return Response({'success':True , 'message':'address deleted !'})
        except Addresses.DoesNotExist :
            return Response({'error':'address not found'}, status=404)