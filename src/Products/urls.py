from django.urls import path
from .views import UserReviews ,EditProduct , VendorsProduct , AddProduct , AllProducts

urlpatterns = [
    path('user_reviews/', UserReviews.as_view() , name='user_reviews'),
    path('add_product/', AddProduct.as_view() , name='add_product'),
    path('vendor_product/', VendorsProduct.as_view() , name='all_product'),
    path('edit_product/<int:pk>/', EditProduct.as_view() , name='edit_product'),

    path('all_product/', AllProducts.as_view() , name='all_product'),
]