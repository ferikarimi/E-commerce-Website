from django.urls import path
from .views import VendorProfile , RegisterVendor , VendorShop , VendorCodeView , RegisterManager , AllShopView , SingleShopView , GetShopProductView
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView


urlpatterns = [
    path('register_vendor_page/', RegisterVendor.as_view() , name='register_vendor'),
    path('vendor_profile/', VendorProfile.as_view() , name='vendor_profile_view'),
    path('vendor_shop/', VendorShop.as_view() , name='Vendor_shop'),

    path('token/', TokenObtainPairView.as_view() , name='Token_Obtain_Pair'),
    path('token/refresh/', TokenRefreshView.as_view() , name='Token_Refresh'),

    path('vendor_code/', VendorCodeView.as_view() , name='vendor_code'),

    path('register_manager_or_operator/', RegisterManager.as_view() , name='register_manager'),
    path('register_manager_or_operator/<str:username>/', RegisterManager.as_view() , name='get_delete_register_manager'),


    path('all_shop/' , AllShopView.as_view() , name='all_shop'),
    path('single_shop/<int:id>/' , SingleShopView.as_view() , name='single_shop'),


    path('get_shop_product/<int:id>/' ,GetShopProductView.as_view() , name='shop_product'),
]