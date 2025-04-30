from django.urls import path
from .views import Cart , FinalCart , VendorOrdersView , UserOrdersView

urlpatterns = [
    #_____________________ cookie _________________________
    # path('set_cookie/', set_cookie , name='set_cookie'),
    # path('get_cookie/', get_cookie , name='get_cookie'),    
    # path('delete_cookie/', delete_cookie, name='delete_cookie'),

    path('cart/', Cart.as_view() , name='add_edit_delete_item_cart'),
    path('finalized_cart/', FinalCart.as_view() , name='finalized_cart'),

    path('vendor_orders/', VendorOrdersView.as_view() , name='get_vendor_orders'),
    path('vendor_orders/<int:id>/', VendorOrdersView.as_view() , name='delete_vendor_orders'),

    path('user_orders/', UserOrdersView.as_view() , name='get_user_orders'),
    path('user_orders/<int:id>/', UserOrdersView.as_view() , name='put_user_orders'),

]