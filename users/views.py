from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserRegistrationSerializer, UserResponseSerializer, UserDetailSerializer, LoginSerializer, LoginResponseSerializer, UserMeSerializer

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        response_serializer = UserResponseSerializer(user)
        
        return Response({
            'message': 'Usuário cadastrado com sucesso!',
            'user': response_serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'message': 'Erro ao cadastrar usuário',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_by_id(request, user_id):
    user = get_object_or_404(User, id=user_id)
    serializer = UserDetailSerializer(user)
    
    return Response({
        'user': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        user.set_online()
        response_serializer = LoginResponseSerializer(user)
        
        return Response({
            'message': 'Login realizado com sucesso!',
            'user': response_serializer.data
        }, status=status.HTTP_200_OK)
    
    return Response({
        'message': 'Erro ao fazer login',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    user = request.user
    serializer = UserMeSerializer(user)
    return Response({
        'user': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    users = User.objects.all().order_by('-created_at')
    serializer = UserDetailSerializer(users, many=True)
    return Response({
        'users': serializer.data,
        'total': users.count()
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    user = request.user
    user.set_offline()
    return Response({
        'message': 'Logout realizado com sucesso!'
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ping_user(request):
    user = request.user
    user.last_seen = timezone.now()
    user.is_online = True
    user.save(update_fields=['last_seen', 'is_online'])
    return Response({
        'message': 'Ping recebido',
        'status': 'online',
        'last_seen': user.last_seen
    }, status=status.HTTP_200_OK)