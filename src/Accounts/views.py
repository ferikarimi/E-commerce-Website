from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer , UserLoginSerializer , UserProfileSerializer
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView


# @csrf_exempt
# @api_view(['POST'])
# def register_user(request):
#     serializer = UserRegisterSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({'user':serializer.data}, status=status.HTTP_201_CREATED)
#     return Response ({'error': serializer.errors} , status=status.HTTP_400_BAD_REQUEST)


class RegisterUser(APIView):
    def post (self , request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=201)
        return Response (serializer.errors , status=400)
        





# @api_view(['POST'])
# def login_user(request):
#     serializer = UserLoginSerializer(data=request.data)
    
#     if serializer.is_valid() :
#         user = serializer.validated_data['user']
#         login(request , user)
#         return Response({'message':'login succes'}, status=status.HTTP_200_OK)
    
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class LoginUser(APIView):
    def post (self , request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid() :
            user = serializer.validated_data['user']
            login(request , user)
            return Response({'message':'login succes'}, status=200)
        return Response(serializer.errors, status=400)





# @api_view(['GET' , 'PUT'])
# def profile_view_user(request):
#     if not request.user.is_authenticated :
#         return Response({'error':'first login then you can see your profile'} , status=status.HTTP_401_UNAUTHORIZED)

#     user = request.user

#     if request.method == 'GET':
#         serializer = UserProfileSerializer(user)
#         return Response(serializer.data , status=status.HTTP_200_OK)
    
#     elif request.method == 'PUT':
#         serializer = UserProfileSerializer(user , data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message':'profile updated !' , 'data':serializer.data},status=status.HTTP_200_OK)
#         return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    



class UserProfile(APIView):

    def get (self , request):
        if not request.user.is_authenticated :
            return Response({'error':'first login then you can see your profile'} , status=401)
        
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data , status=status.HTTP_200_OK)
        

    def put (self , request):
        if not request.user.is_authenticated :
            return Response({'error':'first login then you can see your profile'} , status=401)

        user = request.user
        serializer = UserProfileSerializer(user , data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors , status=400)



@api_view(['GET'])
def check_user_type(request):
    return Response({
        'is_vendor': request.user.is_vendor ,
        'username' : request.user.username
    })