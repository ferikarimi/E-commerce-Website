from django.urls import path
from .views import register_page ,login_page , home_page , user_profile_page , register_vendor_page , user_panel , user_addresses , vendor_profile_page , vendor_panel , add_product , shop_page , all_shop , vendor_product , edit_product , user_reviews , edit_shop , all_product , admin_panel , vendor_code , add_vendor_code , single_product_page , manager_panel , operator_panel , register_operator_or_manager , cart , checkout , thankyou , admin_profile

urlpatterns = [
    # user
    path('user_panel/', user_panel, name='user_panel'),
    path('user_addresses/', user_addresses, name='user_addresses'),
    path('user_reviews/', user_reviews, name='user_reviews'),
    path('profile/', user_profile_page, name='user-profile-page'),

    # vendor
    path('vendor_profile/', vendor_profile_page, name='vendor-profile-page'),
    path('vendor_panel/', vendor_panel, name='vendor-panel'),
    path('edit_shop_details/', edit_shop, name='edit_shop'),
    #____________________________________________________________________________#
    path('register_operator_or_manager/', register_operator_or_manager, name='register_operator_or_manager'),
    path('manager_panel/', manager_panel, name='manager_panel'),
    path('operator_panel/', operator_panel, name='operator_panel'),
    #____________________________________________________________________________#

    # registreation
    path('register/', register_page, name='register_page'),
    path('login/', login_page, name='login_page'),
    path('vendor/', register_vendor_page, name='vendor_home_page'),

    # admin
    path('admin_panel/', admin_panel, name='admin_panel'),
    path('admin_profile/', admin_profile, name='admin_profile'),
    path('add_vendor_code/', add_vendor_code, name='add_vendor_code'),
    path('vendor_code/', vendor_code, name='vendor_code'),

    # product
    path('add_product/', add_product, name='add_product'),
    path('vendor_product/', vendor_product, name='vendor_product'),
    path('all_product/', all_product, name='all_product'),
    path('edit_product/<int:pk>/', edit_product, name='edit_product'),
    path('single_product/<int:pk>/', single_product_page, name='single_product_page'),

    # base
    path('home/', home_page, name='home_page'),
    path('shop_page/<int:pk>/', shop_page, name='shop_page'),
    path('all_shop/', all_shop, name='all_shop'),

    # cart
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('thank_you/' , thankyou , name='tank_you')


]