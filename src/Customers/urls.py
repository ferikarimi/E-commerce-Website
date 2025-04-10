from django.urls import path
from .views import get_addresses , create_address , update_addresses ,  delete_addresses 


urlpatterns = [
    path('addresses/', get_addresses, name='get-addresses'),
    path('address/create', create_address, name='create-address'),
    path('addresses/update', update_addresses, name='update-addresses'),
    path('addresses/delete', delete_addresses, name='delete-addresses'),
]
