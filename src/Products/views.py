from django.shortcuts import get_object_or_404
from .serializers import ReviewsSerializer , AddProductSerializer , VendorProductSerializer , EditProductSerializer , EditSingleProductSerializer , GetSingleProductReviewsSerializer , SingleProductSerializer , SearchProductSerializer , SendReviewsForProductSerializer ,  SendRatingForProductSerializer , ShowProductForReviewsSerializer

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated 
from Vendors.permissions import IsAuthenticatedVendor , IsVendorManager , IsVendorOperator ,IsVendorOrManager
from rest_framework.response import Response
from .models import Reviews , Product
from Vendors.models import Vendors , Shop 
from Cart.models import Orders , OrderDetail
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics , filters
from Accounts.models import User


class UserReviews(APIView):
    """
        get user all reviews
    """
    # permission_classes = [IsAuthenticated]
    
    def get (self , request):
        user = request.user
        user_reviews = Reviews.objects.filter(customer_id=user)
        serializer = ReviewsSerializer(user_reviews , many=True)
        return Response (serializer.data)


class AddProduct(APIView):
    """
        add product 
    """
    # permission_classes = [IsAuthenticatedVendor]
    
    def post (self , request):
        print(f"User: {request.user}, Is Authenticated: {request.user.is_authenticated}")
        vendor = get_object_or_404(Vendors , user=request.user)
        print(f"Vendor Role: {vendor.role}")
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
        all_product = Product.objects.filter(vendor_id = vendor)
        serializer = VendorProductSerializer(all_product , many=True)
        return Response(serializer.data)


class EditProduct (APIView):
    """
        edit product
    """
    # permission_classes = [IsAuthenticatedVendor , IsVendorManager]

    def get (self , request , pk):
        product = get_object_or_404(Product , pk=pk)
        serializer = EditSingleProductSerializer(product)
        return Response (serializer.data)

    def put (self , request , pk):
        product = get_object_or_404(Product , pk=pk)
        serializer = EditProductSerializer (product , data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors , status=400)


class ProductPagination(PageNumberPagination):
    """
        pagination for product page in 'home.html'
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


class SingleProduct(APIView):
    """
        get single product detail
    """
    def get (self , request , id):
        product = get_object_or_404 (Product , id=id)
        serializer = SingleProductSerializer(product)
        return Response (serializer.data , status=200)


















class ProductReviews(APIView):
    """
        get product reviews 
    """
    def get (self , request , id):
        product = get_object_or_404(Product , id=id)
        review = Reviews.objects.filter(product=product ,status='approved')
        serializer = GetSingleProductReviewsSerializer (review , many=True)
        return Response (serializer.data , status=200)
    
    def post (self , request , id):
        product = get_object_or_404(Product, id=id)
        customer = request.user
        serializer = SendReviewsForProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=customer ,product=product)
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
            has_rated = Reviews.objects.filter(customer=user, product=product).exists()
            if not has_rated:
                unrated_products.append(product)


        serializer = ShowProductForReviewsSerializer (unrated_products , many=True)
        return Response (serializer.data , status=200)

    def post(self , request):
        serializer = SendRatingForProductSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=201)
        return Response(serializer.errors , status=400)