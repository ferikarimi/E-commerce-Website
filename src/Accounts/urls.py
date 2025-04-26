from django.urls import path
from .views import  UserProfile , CheckUserType , RegisterUser , Logout


urlpatterns = [
    path('register/', RegisterUser.as_view() , name='register'),
    path('user_profile/', UserProfile.as_view() , name='user_profile'),
    path('check_user_type/', CheckUserType.as_view() , name='check_user_type'),
    path('logout/', Logout.as_view() , name='logout'),
]