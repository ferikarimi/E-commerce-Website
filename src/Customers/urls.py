from django.urls import path
from .views import  GetUserAddresses


urlpatterns = [
    path('address/', GetUserAddresses.as_view() , name='get-post-addresses'),
    path('address/<int:id>/', GetUserAddresses.as_view() , name='put-delete-addresses'),
]