from rest_framework.response import Response
from .serializers import VendorRegisterSerializer , VendorProfileSerializer , VendorShopSerializer , VendorCodeSerializer , RegisterManagerSerializer , ManagerSerializer , AllShopSerializer , SingleShopSerializer , ShowOneShopProductsSerializer
from rest_framework.permissions import IsAuthenticated , IsAdminUser , AllowAny
from .models import Vendors , VendorCode 
from rest_framework.views import APIView
from .permissions import IsAuthenticatedVendor , IsVendorManager , IsVendorOperator
from django.shortcuts import get_object_or_404
from Products.models import Shop ,Product
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics





class RegisterVendor (APIView):
    """
        register a vendor and create a single shop for vendor
    """
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
    """
        get and update vendor profile
    """
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
    """
        get and update vendor`s shop
    """
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
    """
        admin can add a number for register a vendor
    """
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
    """
        vendor can employee manager and operator
    """
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
    
































class ShopPagination (PageNumberPagination):
    """
        pagination all shop page
    """
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 12
    

class AllShopView(generics.ListAPIView):
    """
        get all shop
    """
    permission_classes = [AllowAny]
    shops = Shop.objects.all()
    serializer_class = AllShopSerializer
    pagination_class = ShopPagination

    def get_queryset(self):
        shops = Shop.objects.all()
        sort_by = self.request.query_params.get('sort')

        if sort_by == 'badseller':
            shops = shops.order_by('product_sold_count')

        elif sort_by == 'bestseller':
            shops = shops.order_by('-product_sold_count')

        elif sort_by == 'oldest':
            shops = shops.order_by('created_at')
        
        else :
            shops = shops.order_by('-created_at')
        
        return shops


class SingleShopView(APIView):
    """
        show single shop detail
    """
    permission_classes = [AllowAny]

    def get (self , request , id):
        shop = get_object_or_404(Shop , id=id)
        serializer = SingleShopSerializer (shop)
        return Response (serializer.data , status=200)


class GetShopProductView (APIView):
    """
        show products of shop
    """
    permission_classes = [AllowAny]

    def get (self , request , id):
        shop = get_object_or_404(Shop ,id=id)
        products = Product.objects.filter(store_name=shop)
        serializer = ShowOneShopProductsSerializer (products , many=True)
        return Response (serializer.data , status=200)
    


class SearchShop(APIView):
    """
        search shop by 'name','field'
    """
    pass