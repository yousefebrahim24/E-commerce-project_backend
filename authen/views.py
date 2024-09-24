# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
# from rest_framework.response import Response
# from django.contrib.auth.models import User
# from django.contrib.auth.hashers import make_password
# from rest_framework_simplejwt.tokens import RefreshToken
# from .serializers import UserSerializer, UserSerializerWithToken

# @api_view(['POST'])
# def registerUser(request):
#     data = request.data
#     try:
#         user = User.objects.create(
#             username=data['username'],
#             email=data['email'],
#             password=make_password(data['password'])
#         )
#         serializer = UserSerializerWithToken(user, many=False)
#         return Response(serializer.data)
#     except:
#         return Response({'detail': 'User with this email already exists'}, status=400)

# @api_view(['POST'])
# def login(request):
#     # You will use Simple JWT's default views for login/logout
#     pass

# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def updateUserProfile(request):
#     user = request.user
#     serializer = UserSerializerWithToken(user, many=False)

#     data = request.data
#     user.first_name = data['first_name']
#     user.last_name = data['last_name']
#     user.email = data['email']

#     if data['password'] != '':
#         user.password = make_password(data['password'])

#     user.save()
#     return Response(serializer.data)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def getUserProfile(request):
#     user = request.user
#     serializer = UserSerializer(user, many=False)
#     return Response(serializer.data)

# @api_view(['GET'])
# @permission_classes([IsAdminUser])
# def getUsers(request):
#     users = User.objects.all()
#     serializer = UserSerializer(users, many=True)
#     return Response(serializer.data)

# @api_view(['DELETE'])
# @permission_classes([IsAdminUser])
# def deleteUser(request, pk):
#     user = User.objects.get(id=pk)
#     user.delete()
#     return Response({'detail': 'User was deleted'})

# @api_view(['GET'])
# @permission_classes([IsAdminUser])
# def getUserById(request, pk):
#     user = User.objects.get(id=pk)
#     serializer = UserSerializer(user, many=False)
#     return Response(serializer.data)

# @api_view(['PUT'])
# @permission_classes([IsAdminUser])
# def updateUser(request, pk):
#     user = User.objects.get(id=pk)

#     data = request.data
#     user.first_name = data['first_name']
#     user.last_name = data['last_name']
#     user.email = data['email']
#     user.is_staff = data['isAdmin']

#     user.save()
#     serializer = UserSerializer(user, many=False)
#     return Response(serializer.data)







# from django.contrib.auth import authenticate
# from django.contrib.auth.models import User
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken
# from .serializers import RegisterSerializer

# @api_view(['POST'])
# def register_user(request):
#     serializer = RegisterSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def login_user(request):
#     username = request.data.get('username')
#     password = request.data.get('password')
#     user = authenticate(username=username, password=password)

#     if user is not None:
#         refresh = RefreshToken.for_user(user)
#         return Response({
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#         })
#     else:
#         return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)









from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import (
    RegisterSerializer, 
    UserSerializer, 
    UpdateUserProfileSerializer, 
    CustomTokenObtainPairSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView

# Register User
@api_view(['POST'])
def registerUser(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login User
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Update User Profile
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    serializer = UpdateUserProfileSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Get User Profile
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user 
    serializer = UserSerializer(user)
    return Response(serializer.data)

# Get All Users (Admin Only)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

# Get User by ID (Admin Only)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user)
    return Response(serializer.data)

# Delete User (Admin Only)
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    user = User.objects.get(id=pk)
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Update User (Admin Only)
@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateUser(request, pk):
    user = User.objects.get(id=pk)
    serializer = UpdateUserProfileSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

