from django.shortcuts import get_object_or_404
from .serializers import ReviewsSerializer , AddProductSerializer , AllProductSerializer , VendorProductSerializer , EditProductSerializer , ShowSingleSerializer , SingleProductReviewsSerializer , SingleProductSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Reviews , Product
from Vendors.models import Vendors , Shop
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics



class UserReviews(APIView):
    permission_classes = [IsAuthenticated]
    
    def get (self , request):
        user = request.user
        user_reviews = Reviews.objects.filter(customer_id=user)
        serializer = ReviewsSerializer(user_reviews , many=True)
        return Response (serializer.data)


class AddProduct(APIView):
    
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

    def get(self , request):
        vendor = Vendors.objects.get(user=request.user)
        all_product = Product.objects.filter(vendor_id = vendor)
        serializer = VendorProductSerializer(all_product , many=True)
        return Response(serializer.data)


class EditProduct (APIView):
    def get (self , request , pk):
        product = get_object_or_404(Product , pk=pk)
        serializer = ShowSingleSerializer(product)
        return Response (serializer.data)

    def put (self , request , pk):
        product = get_object_or_404(Product , pk=pk)
        serializer = EditProductSerializer (product , data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors , status=400)
    

class ProductPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 16


class AllProducts(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = AllProductSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        queryset = Product.objects.all()
        sort_by = self.request.query_params.get('sort')
        
        if sort_by == 'cheap':
            queryset = queryset.order_by('price')

        elif sort_by == 'expensive':
            queryset = queryset.order_by('-price')

        elif sort_by == 'lowest_score':
            queryset = queryset.order_by('rating')

        elif sort_by == 'highest_score':
            queryset = queryset.order_by('-rating')

        elif sort_by == 'badseller':
            queryset = queryset.order_by('sold_count')

        elif sort_by == 'bestseller':
            queryset = queryset.order_by('-sold_count')

        elif sort_by == 'oldest':
            queryset = queryset.order_by('created_at')
        
        else :
            queryset = queryset.order_by('-created_at')
        
        return queryset
    














class ProductReviews(APIView):
    def get (self , request , id):
        product = get_object_or_404(Product , id=id)
        review = Reviews.objects.filter(product=product ,status='approved')
        serializer = SingleProductReviewsSerializer (review , many=True)
        return Response (serializer.data , status=200)
    


class SingleProduct(APIView):
    def get (self , request , id):
        product = get_object_or_404 (Product , id=id)
        serializer = SingleProductSerializer(product)
        return Response (serializer.data , status=200)