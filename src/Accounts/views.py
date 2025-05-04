from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer , UserProfileSerializer
from rest_framework.permissions import IsAuthenticated , AllowAny
from Vendors.permissions import IsAuthenticatedVendor , IsVendorManager , IsVendorOperator
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken



class RegisterUser(APIView):
    """
        register user with jwt
    """
    permission_classes = [AllowAny]

    def post (self , request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access' : str(refresh.access_token)
            } , status=201)
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

    def put (self , request):
        user = request.user
        serializer = UserProfileSerializer(user , data=request.data)
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