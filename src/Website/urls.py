from django.urls import path
from .views import AllShopView , SingleShopView , GetShopProductView

urlpatterns=[
    path('all_shop/' , AllShopView.as_view() , name='all_shop'),
    path('single_shop/<int:id>/' , SingleShopView.as_view() , name='single_shop'),
    path('get_shop_product/<int:id>/' ,GetShopProductView.as_view() , name='get_shop_product'),
]