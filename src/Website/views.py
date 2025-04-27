from django.shortcuts import render , redirect
from Products.models import Shop ,Product
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .serializers import AllShopSerializer , SingleShopSerializer , ShowOneShopProductsSerializer

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated , IsAdminUser , AllowAny

from django.shortcuts import get_object_or_404








class AllShopView(APIView):
    def get (self , request):
        try:
            shops = Shop.objects.all()
            serializer = AllShopSerializer (shops , many=True)
            return Response (serializer.data , status=200)
        except Exception as e :
            return Response ({'error':'unable to load shops'} , status=404)


class SingleShopView(APIView):
    def get (self , request , id):
        shop = get_object_or_404(Shop , id=id)
        serializer = SingleShopSerializer (shop)
        return Response (serializer.data , status=200)

class GetShopProductView (APIView):
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