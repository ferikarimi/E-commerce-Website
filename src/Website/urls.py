from django.urls import path
from .views import product_list_view 

urlpatterns=[
    path('home/' , product_list_view , name='product-list')
]