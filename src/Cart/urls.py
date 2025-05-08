from django.urls import path
from .views import Cart , CheckOutView , VendorOrdersView , UserOrdersView , UserOrderDetail

urlpatterns = [
    path('cart/', Cart.as_view() , name='add_edit_delete_item_cart'),
    path('finalized_cart/', CheckOutView.as_view() , name='finalized_cart'),
    path('vendor_orders/', VendorOrdersView.as_view() , name='get_vendor_orders'),
    path('vendor_orders/<int:id>/', VendorOrdersView.as_view() , name='delete_vendor_orders'),
    path('user_orders/', UserOrdersView.as_view() , name='get_user_orders'),
    path('user_orders/<int:id>/', UserOrdersView.as_view() , name='put_user_orders'),
    path('user_order_detail/<int:id>/', UserOrderDetail.as_view() , name='user-order-detail'),
]