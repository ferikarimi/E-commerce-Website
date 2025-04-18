from django.shortcuts import render , redirect
from Products.models import Product
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .serializers import ProductSerializer


# from django.http import HttpResponseBadRequest
# from .urls import create_token_view
# from .tasks import send_otp_code
# from .redis_setup import client



@api_view(['GET'])
def product_list_view(request):
    products = Product.objects.all()
    category_id = request.GET.get('category_id')
    vendor_id = request.GET.get('vendor_id')
    ordering = request.GET.get('ordering')

    if category_id :
        products = products.filter(category_id=category_id)

    if vendor_id :
        products = products.filter(vendor_id=vendor_id)

    if ordering in ['price' , '-price' , 'rating' , '-rating', 'sold_count' ,'-sold_count']:
        products = products.order_by(ordering)

    paginator = PageNumberPagination()
    paginator.page_size = 5
    result_page = paginator.paginate_queryset(products , request)
    serialiazer = ProductSerializer(result_page , many=True)
    return paginator.get_paginated_response(serialiazer.data)






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