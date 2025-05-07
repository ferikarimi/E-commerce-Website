from django.urls import path
from .views import UserComments ,EditProduct , VendorsProduct , AddProduct , SearchProducts , ProductComments , SingleProduct , SendRatingForProduct

urlpatterns = [
    path('user_comments/', UserComments.as_view() , name='user_comments'),
    path('add_product/', AddProduct.as_view() , name='add_product'),
    path('vendor_product/', VendorsProduct.as_view() , name='all_product'),
    path('edit_product/<int:pk>/', EditProduct.as_view() , name='edit_product'),
    path('all_product/', SearchProducts.as_view() , name='all_product'),
    path('product_comments/<int:id>/', ProductComments.as_view() , name='product_comments'),
    path('single_product/<int:id>/', SingleProduct.as_view() , name='single_product'),
    path('send_rating_for_product/', SendRatingForProduct.as_view() , name='send-rating-for-product'),
]