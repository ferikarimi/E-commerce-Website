from django.urls import path
from .views import register_user , login_user , register_vendor , user_profile_view


urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login_user/', login_user, name='login_user'),
    path('register_vendor/', register_vendor, name='register_vendor'),
    path('user_profile_view/', user_profile_view, name='user_profile_view'),

]
