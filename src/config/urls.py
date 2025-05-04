from django.urls import path
from .views import register_page ,login_page  , user_profile_page , register_vendor_page , user_panel , user_addresses , vendor_profile_page , vendor_panel , add_product , shop_page , all_shop , vendor_product , edit_product , user_reviews , edit_shop , all_product , admin_panel , vendor_code , add_vendor_code , single_product_page , manager_panel , operator_panel , register_operator_or_manager , cart , checkout , thankyou , admin_profile , user_order , vendor_order , manage_reviews , product_rating

urlpatterns = [
    #________________________________ user _____________________________________
    path('user_panel/', user_panel, name='user-panel'),
    path('user_addresses/', user_addresses, name='user-addresses'),
    path('user_reviews/', user_reviews, name='user-reviews'),
    path('profile/', user_profile_page, name='user-profile-page'),
    path('user_order/', user_order, name='user-order'),
    
    path('product_rating/', product_rating, name='product-rating'),
    #____________________________________________________________________________

    #________________________________ vendor _____________________________________
    path('vendor_profile/', vendor_profile_page, name='vendor-profile-page'),
    path('vendor_panel/', vendor_panel, name='vendor-panel'),
    path('edit_shop_details/', edit_shop, name='edit-shop'),
    path('vendor_order/', vendor_order, name='vendor-order'),
    path('register_operator_or_manager/', register_operator_or_manager, name='register-operator-or-manager'),
    path('manager_panel/', manager_panel, name='manager-panel'),
    path('operator_panel/', operator_panel, name='operator-panel'),

    path('manage_reviews/', manage_reviews, name='manage-reviews'),
    #____________________________________________________________________________

    #_______________________________ registreation ______________________________
    path('register/', register_page, name='register-page'),
    path('login/', login_page, name='login-page'),
    path('vendor/', register_vendor_page, name='vendor-home-page'),
    #____________________________________________________________________________

    #_______________________________ admin ______________________________________
    path('admin_panel/', admin_panel, name='admin-panel'),
    path('admin_profile/', admin_profile, name='admin-profile'),
    path('add_vendor_code/', add_vendor_code, name='add-vendor-code'),
    path('vendor_code/', vendor_code, name='vendor-code'),
    #____________________________________________________________________________

    #_______________________________ product ____________________________________
    path('add_product/', add_product, name='add-product'),
    path('vendor_product/', vendor_product, name='vendor-product'),
    path('all_product/', all_product, name='all-product'),
    path('edit_product/<int:pk>/', edit_product, name='edit-product'),
    path('single_product/<int:pk>/', single_product_page, name='single-product-page'),
    #____________________________________________________________________________


    #_______________________________ base _______________________________________
    path('shop_page/<int:pk>/', shop_page, name='shop-page'),
    path('all_shop/', all_shop, name='all-shop'),
    #____________________________________________________________________________



    #__________________________________ cart ____________________________________
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('thank_you/' , thankyou , name='thank-you')
    #____________________________________________________________________________
]