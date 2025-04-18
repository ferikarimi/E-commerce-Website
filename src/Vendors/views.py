from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import VendorRegisterSerializer , VendorProfileSerializer , VendorShopSerializer
from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .models import Vendors , Shop
from rest_framework.views import APIView
from .permissions import IsAuthenticatedVendor



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
        vendor = Vendors.objects.get(user=request.user)
        serializer = VendorProfileSerializer(vendor)
        return Response (serializer.data , status=200)
    
    def put (self , request):
        vendor = Vendors.objects.get(user=request.user)
        serializer = VendorProfileSerializer(vendor , data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'profile updated successfuly !'} , status=200)
        return Response(serializer.errors , status=400)


class VendorShop(APIView):
    permission_classes = [IsAuthenticatedVendor]

    def get(self, request):
        try:
            vendor = Vendors.objects.get(user=request.user)
            vendor_shop = Shop.objects.get(vendor=vendor)
        except (Vendors.DoesNotExist, Shop.DoesNotExist):
            return Response({'error': 'Vendor or shop not found'}, status=404)
        
        serializer = VendorShopSerializer(vendor_shop)
        return Response(serializer.data, status=200)


    def put(self, request):
        try:
            vendor = Vendors.objects.get(user=request.user)
            vendor_shop = Shop.objects.get(vendor=vendor)
        except (Vendors.DoesNotExist, Shop.DoesNotExist):
            return Response({'error': 'Vendor or shop not found'}, status=404)

        serializer = VendorShopSerializer(vendor_shop, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Shop detail updated successfully!'}, status=200)
        return Response(serializer.errors, status=400)


























def store_page(request):
    pass