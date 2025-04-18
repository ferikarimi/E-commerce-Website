from django.urls import path
from .views import  GetUserAddresses , CreateAddress , UpdateAddress , DeleteAddress


urlpatterns = [
    path('address/all', GetUserAddresses.as_view() , name='get-addresses'),
    path('address/create', CreateAddress.as_view() , name='create-address'),
    path('address/update', UpdateAddress.as_view() , name='update-addresses'),
    path('address/delete/<int:id>', DeleteAddress.as_view() , name='delete-addresses'),
]
