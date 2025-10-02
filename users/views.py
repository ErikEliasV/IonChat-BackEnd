from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .serializers import UserRegistrationSerializer, UserResponseSerializer, UserDetailSerializer

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