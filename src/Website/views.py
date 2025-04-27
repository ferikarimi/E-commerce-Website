from django.shortcuts import render , redirect
from Products.models import Shop ,Product
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .serializers import AllShopSerializer , SingleShopSerializer , ShowOneShopProductsSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated , IsAdminUser , AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics


class ShopPagination (PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 12
    

class AllShopView(generics.ListAPIView):
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
    permission_classes = [AllowAny]

    def get (self , request , id):
        shop = get_object_or_404(Shop , id=id)
        serializer = SingleShopSerializer (shop)
        return Response (serializer.data , status=200)

class GetShopProductView (APIView):
    permission_classes = [AllowAny]

    def get (self , request , id):
        shop = get_object_or_404(Shop ,id=id)
        products = Product.objects.filter(store_name=shop)
        serializer = ShowOneShopProductsSerializer (products , many=True)
        return Response (serializer.data , status=200)






# from django.http import HttpResponseBadRequest
# from .urls import create_token_view
# from .tasks import send_otp_code
# from .redis_setup import client

# def otp_generation_view (request):
#     if request.method == 'POST':
#         otp_token = request.POST.get('otp_token')
#         valid_token = client.hget("token","token")
#         str_valid_token = valid_token.decode('utf-8')
#         if otp_token == str_valid_token :
#             response = redirect("home")
#             token = create_token_view("sample")
#             print(token)
#             response.set_cockie("token", token , max_age=300)
#             return response
#         else:
#             return HttpResponseBadRequest("invalid OTP")
#     return render (request , "registration/otp_generatecode.html")