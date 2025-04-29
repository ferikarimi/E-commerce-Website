from django.urls import path
from .views import Cart , FinalCart

urlpatterns = [
    #_____________________ cookie _________________________
    # path('set_cookie/', set_cookie , name='set_cookie'),
    # path('get_cookie/', get_cookie , name='get_cookie'),    
    # path('delete_cookie/', delete_cookie, name='delete_cookie'),

    path('cart/', Cart.as_view() , name='add_edit_delete_item_cart'),
    path('finalized_cart/', FinalCart.as_view() , name='finalized_cart'),

]