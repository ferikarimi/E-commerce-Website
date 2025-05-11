from rest_framework.response import Response
from .serializers import UserRegisterSerializer , UserProfileSerializer
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
import random
from django.core.mail import send_mail
from .models import User
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from kavenegar import *
from .utils import rate_limit


class RegisterUser(APIView):
    """
        register user
    """
    permission_classes = [AllowAny]

    def post (self , request):
        serializer = UserRegisterSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=201)
        return Response (serializer.errors , status=400)


class UserProfile(APIView):
    """
        get and update user profile 
    """
    permission_classes = [IsAuthenticated]

    def get (self , request):        
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data , status=200)

    def patch (self , request):
        request.data.pop('created_at_shamsi', None)
        user = request.user
        serializer = UserProfileSerializer(user , data=request.data , partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    

class Logout (APIView):
    """
        log out user and blocked jwt token 
    """
    permission_classes = [IsAuthenticated]

    def post (self , request):
        try :
            refresh = request.data['refresh_token']
            token = RefreshToken(refresh)
            token.blacklist()
            return Response(status=205)
        except Exception as error :
            return Response (status=400)


class CheckUserType (APIView):
    """
        check user type
    """
    def get (self, request):
        return Response ({
            'username' : request.user.username ,
            'is_superuser': request.user.is_superuser ,
            'is_vendor': request.user.is_vendor ,
            'is_customer': request.user.is_customer
        })


# -------------------- otp with redis cache -------------------#
def generate_otp (email_or_phone , timeout=120):
    otp = str(random.randint(100000 , 999999))
    cache.set(email_or_phone ,otp,timeout=timeout)
    return otp

def get_otp (email_or_phone):
    return cache.get(email_or_phone)

def delete_otp (email_or_phone):
    cache.delete(email_or_phone)
# ------------------------------------------------------------#

class CustomLoginView(APIView):
    """
        custom login with otp verification and create jwt token
    """
    @rate_limit
    def post (self ,request):
        email = request.data.get('email')
        phone = request.data.get('phone')
        if not email and not phone:
            return Response({'error': 'email or phone is required'}, status=400)

        if email :
            try:
                # otp = generate_otp(phone)
                # print('------------ OTP code for email --------------')
                # print(f'otp : {otp}')
                # print('-----------------------------------------------')
                otp = generate_otp(email)
                send_mail(
                    subject='your OTP code',
                    message=f'your OPT code is : {otp}',
                    from_email= 'farzad3467@gmail.com',
                    recipient_list=[email],
                )
                return Response ({'message':'OTP send successfully'}, status=200)
            except APIException as e :
                return Response ({'error':str(e)}, status=400)

        elif phone :
            try:
                otp = generate_otp(phone)
                print('------------ OTP code for mobile --------------')
                print(f'otp : {otp}')
                print('-----------------------------------------------')

                # otp = generate_otp(phone)
                # api = KavenegarAPI('556D6F4E684E74342B74516F4F6A694372593338786D4B646A2F554A736D464C5648794535595173306F773D')
                # params = {
                #     'sender': '20006535',
                #     'receptor': '09305489152',
                #     'message': f'کد تایید شما: {otp}',
                # }
                # print(params)

                # api.sms_send(params)
                # print('sms_send')

                return Response({'message':'OTP code send'},status=200)
            except APIException as e :
                return Response ({'error':str(e)}, status=400)


class VerifyOTPView(APIView):
    """
        verifu otp code and delete otp
    """
    def post (self , request):
        email = request.data.get('email')
        phone = request.data.get('phone')
        otp = request.data.get('otp')

        email_or_phone = email if email else phone
        cached_otp = get_otp(email_or_phone)

        if cached_otp == otp:
            delete_otp(email_or_phone)
            user = get_object_or_404(User, email=email) if email else get_object_or_404(User, phone=phone)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=200)
        else:
            return Response({'error': 'Invalid or expired OTP'}, status=400)
        

# get access token f