from django.shortcuts import get_object_or_404
from .serializers import CommentsSerializer , AddProductSerializer , VendorProductSerializer , EditProductSerializer , GetSingleProductCommentsSerializer , SingleProductSerializer , SearchProductSerializer , SendCommentsForProductSerializer ,  SendRatingForProductSerializer , ShowProductForRatingSerializer

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated , AllowAny
from Vendors.permissions import IsAuthenticatedVendor , IsVendorManager , IsVendorOperator ,IsVendorOrManager
from rest_framework.response import Response
from .models import Product , Rating , Comments
from Vendors.models import Vendors , Shop 
from Cart.models import Orders , OrderDetail
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics , filters
from Accounts.models import User



class UserComments(APIView):
    """
        get all comments of single user
    """
    # permission_classes = [IsAuthenticated]
    
    def get (self , request):
        user = request.user
        user_comments = Comments.objects.filter(customer_id=user)
        serializer = CommentsSerializer(user_comments , many=True)
        return Response (serializer.data)


class AddProduct(APIView):
    """
        vendor can add product to shop
    """
    # permission_classes = [IsAuthenticatedVendor]
    
    def post (self , request):
        vendor = get_object_or_404(Vendors , user=request.user)
        shop = get_object_or_404(Shop , vendor=vendor)
        serializer = AddProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                vendor_id = vendor.id ,
                store_name = shop
            )
            return Response({'message':'product created !'} , status=201)
        return Response(serializer.errors , status=400)


class VendorsProduct(APIView):
    """
        get vendor products
    """
    # permission_classes = [IsAuthenticatedVendor]

    def get(self , request):
        vendor = Vendors.objects.get(user=request.user)
        vendor_product = Product.objects.filter(vendor_id = vendor)
        serializer = VendorProductSerializer(vendor_product , many=True)
        return Response(serializer.data)


class EditProduct (APIView):
    """
        vendor can edit products
    """
    # permission_classes = [IsAuthenticatedVendor , IsVendorManager]

    def get (self , request , id):
        product = get_object_or_404(Product , id=id)
        serializer = EditProductSerializer(product)
        return Response (serializer.data)

    def patch (self , request , id):
        product = get_object_or_404(Product , id=id)
        serializer = EditProductSerializer (product , data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors , status=400)


class ProductPagination(PageNumberPagination):
    """
        pagination for products
    """
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 16


class SearchProducts(generics.ListAPIView):
    """
        get all product for 'home.html' page 
              searching and sorting
    """
    
    queryset = Product.objects.all()
    serializer_class = SearchProductSerializer
    pagination_class = ProductPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name','category__name','store_name__name']

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.query_params.get('sort')
        
        if sort_by == 'cheap':
            queryset = queryset.order_by('price')

        elif sort_by == 'expensive':
            queryset = queryset.order_by('-price')

        elif sort_by == 'lowest_score':
            queryset = queryset.order_by('average_rating')

        elif sort_by == 'highest_score':
            queryset = queryset.order_by('-average_rating')

        elif sort_by == 'badseller':
            queryset = queryset.order_by('sold_count')

        elif sort_by == 'bestseller':
            queryset = queryset.order_by('-sold_count')

        elif sort_by == 'oldest':
            queryset = queryset.order_by('created_at')
        
        else :
            queryset = queryset.order_by('-created_at')
        
        return queryset


class SingleProduct(APIView):
    """
        get single product detail
    """
    def get (self , request , id):
        product = get_object_or_404 (Product , id=id)
        serializer = SingleProductSerializer(product)
        return Response (serializer.data , status=200)


class ProductComments(APIView):
    """
        get single product Comments 
    """
    permission_classes = [AllowAny]
    def get (self , request , id):
        product = get_object_or_404(Product , id=id)
        review = Comments.objects.filter(product=product ,status='approved')
        serializer = GetSingleProductCommentsSerializer (review , many=True)
        return Response (serializer.data , status=200)
    
    def post (self , request , id):
        product = get_object_or_404(Product, id=id)
        user = request.user
        serializer = SendCommentsForProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=user ,product=product)
            return Response(serializer.data , status=201)
        return Response(serializer.errors , status=400)


class SendRatingForProduct(APIView):
    """
        user can Register rate for the purchased product
    """
    permission_classes = [IsAuthenticated]
    def get (self , request):
        user = request.user
        delivered_order = Orders.objects.filter(customer=user , status="delivered")
        order_detail = OrderDetail.objects.filter(order__in=delivered_order)
        purchased_products = [order.product for order in order_detail]

        unrated_products = []
        for product in purchased_products:
            has_rated = Rating.objects.filter(customer=user, product=product).exists()
            if not has_rated:
                unrated_products.append(product)
        serializer = ShowProductForRatingSerializer (unrated_products , many=True)
        return Response (serializer.data , status=200)

    def post(self , request):
        serializer = SendRatingForProductSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=201)
        else:
            return Response(serializer.errors , status=400)