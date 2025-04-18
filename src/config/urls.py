from django.urls import path
from .views import register_page ,login_page , home_page , user_profile_page , register_vendor_page , user_panel , user_addresses , vendor_profile_page , vendor_panel , add_product , store_page , vendor_product , edit_product , user_reviews , edit_shop , all_product


urlpatterns = [
    path('user_panel/', user_panel, name='user_panel'),#
    path('user_addresses/', user_addresses, name='user_addresses'),#
    path('register/', register_page, name='register_page'),#
    path('login/', login_page, name='login_page'),#
    path('profile/', user_profile_page, name='user-profile-page'),#
    path('vendor_profile/', vendor_profile_page, name='vendor-profile-page'),#
    path('vendor_panel/', vendor_panel, name='vendor-panel'),#


    path('user_reviews/', user_reviews, name='user_reviews'),
    path('vendor_product/', vendor_product, name='all_product'),


    path('home/', home_page, name='home_page'),
    path('vendor/', register_vendor_page, name='vendor_home_page'),
    path('add_product/', add_product, name='add_product'),
    path('vendor_product/', vendor_product, name='vendor_product'),
    path('all_product/', all_product, name='all_product'),

    path('edit_product/<int:pk>/', edit_product, name='edit_product'),
    path('store_page/', store_page, name='store_page'),

    path('edit_shop_details/', edit_shop, name='edit_shop'),

]