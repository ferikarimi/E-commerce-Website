from django.urls import path
from .views import LoginUser , UserProfile , check_user_type , RegisterUser


urlpatterns = [

    path('register/', RegisterUser.as_view() , name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('user_profile/', UserProfile.as_view() , name='user_profile'),
    path('check_user_type/', check_user_type, name='check_user_type'),
]