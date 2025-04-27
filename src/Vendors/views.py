from rest_framework.response import Response
from .serializers import VendorRegisterSerializer , VendorProfileSerializer , VendorShopSerializer , VendorCodeSerializer , RegisterManagerSerializer , ManagerSerializer
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from .models import Vendors , Shop , VendorCode
from rest_framework.views import APIView
from .permissions import IsAuthenticatedVendor 
from django.shortcuts import get_object_or_404
from Accounts.models import User



class RegisterVendor (APIView):
    permission_classes = [IsAuthenticated]

    def post (self , request):
        if request.user.is_vendor :
            return Response ({'error':'you r already vendor'} , status=400)
        
        serializer = VendorRegisterSerializer(data=request.data , context={'request':request})
        if serializer.is_valid():
            vendor = serializer.save()
            user = vendor.user
            user.is_vendor = True
            user.is_customer = False
            user.save()
            return Response({'message':'vendor succeessfully registered !'} , status=201)
        return Response(serializer.errors , status=400)



class VendorProfile(APIView):
    permission_classes = [IsAuthenticatedVendor]

    def get (self , request):
        vendor = get_object_or_404(Vendors ,user=request.user)
        serializer = VendorProfileSerializer(vendor)
        return Response (serializer.data , status=200)
    
    def put (self , request):
        vendor = get_object_or_404(Vendors ,user=request.user)
        serializer = VendorProfileSerializer(vendor , data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'profile updated successfuly !'} , status=200)
        return Response(serializer.errors , status=400)



class VendorShop(APIView):
    permission_classes = [IsAuthenticatedVendor]

    def get(self, request):
        vendor = get_object_or_404(Vendors , user=request.user)
        vendor_shop = get_object_or_404(Shop , vendor=vendor)
        serializer = VendorShopSerializer(vendor_shop)
        return Response(serializer.data, status=200)

    def put(self, request):
        vendor = get_object_or_404(Vendors , user=request.user)
        vendor_shop = get_object_or_404(Shop ,vendor=vendor)
        serializer = VendorShopSerializer(vendor_shop, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Shop detail updated successfully!'}, status=200)
        return Response(serializer.errors, status=400)


class VendorCodeView (APIView):
    permission_classes = [IsAdminUser]

    def get (self , request):
        vendor_code = VendorCode.objects.all()
        serializer = VendorCodeSerializer (vendor_code , many=True)
        return Response (serializer.data , status=200)

    def post (self , request):
        serializer = VendorCodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data , status=201)
        return Response (serializer.errors, status=400)
    


class RegisterManager (APIView):
    permission_classes = [IsAuthenticatedVendor]

    def get (self , request):
        vendor = request.user.vendors
        member = vendor.vendor_member.all()
        serializer = ManagerSerializer(member , many=True)
        return Response(serializer.data , status=200)

    def post (self , request):
        serializer = RegisterManagerSerializer(data=request.data , context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=201)
        return Response(serializer.errors , status=400)

    def delete (self , request , username):
        vendor = get_object_or_404(Vendors , user__username=username)
        vendor.user.is_vendor = False
        vendor.user.is_customer = True
        vendor.user.save()
        vendor.delete()
        return Response({"message": "فروشنده با موفقیت حذف شد."}, status=200)













# class RegisterOperator (APIView):
#     permission_classes = [IsAuthenticatedVendor]

#     pass