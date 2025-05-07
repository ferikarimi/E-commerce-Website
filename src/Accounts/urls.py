from django.urls import path
from .views import  UserProfile , CheckUserType , RegisterUser , Logout , VerifyOTPView , CustomLoginView


urlpatterns = [
    path('register/', RegisterUser.as_view() , name='register'),
    path('user_profile/', UserProfile.as_view() , name='user-profile'),
    path('check_user_type/', CheckUserType.as_view() , name='check-user-type'),
    path('logout/', Logout.as_view() , name='logout'),
    path('login/', CustomLoginView.as_view() , name='login-with-otp'),
    path('verify_otp/', VerifyOTPView.as_view() , name='verify-otp'),
]