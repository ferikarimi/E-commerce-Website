from django.urls import path
from .views import VendorProfile , RegisterVendor , VendorShop
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView


urlpatterns = [
    path('register_vendor_page/', RegisterVendor.as_view() , name='register_vendor'),
    path('vendor_profile/', VendorProfile.as_view() , name='vendor_profile_view'),
    path('vendor_shop/', VendorShop.as_view() , name='Vendor_shop'),

    path('token/', TokenObtainPairView.as_view() , name='Token_Obtain_Pair'),
    path('token/refresh/', TokenRefreshView.as_view() , name='Token_Refresh'),
]