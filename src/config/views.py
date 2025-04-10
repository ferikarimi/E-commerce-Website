from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerRegisterSerializer , LoginSerializer , VendorRegisterSerializer , UserProfileSerializer
from django.contrib.auth import login


@api_view(['POST'])
def register_user(request):
    serializer = CustomerRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'user':serializer.data}, status=status.HTTP_201_CREATED)

    return Response ({'error': serializer.errors} , status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def login_user(request):
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid() :
        user = serializer.validated_data['user']
        login(request , user)

        return Response({'message':'login succes'}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register_vendor(request):
    if not request.user.is_authenticated :
        return Response({'error':'first login then reegister a shop'} , status=status.HTTP_401_UNAUTHORIZED)

    serializer = VendorRegisterSerializer(data=request.data , context={'request':request})
    if serializer.is_valid():
        serializer.save()
        return Response({'message':'vendor succeessfully registered !'} , status=status.HTTP_201_CREATED)
    return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET' , 'PUT'])
def user_profile_view(request):
    user = request.user

    if request.method == 'GET':
        serializer = UserProfileSerializer(user)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = UserProfileSerializer(user , data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'profile updated !' , 'data':serializer.data},status=status.HTTP_200_OK)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)