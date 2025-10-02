from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'password_confirm')
        
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email já está em uso.")
        return value
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                "password_confirm": "As senhas não coincidem."
            })
        return attrs
        
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        validated_data['username'] = validated_data['email']
        user = User.objects.create_user(**validated_data)
        return user


class UserResponseSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class UserDetailSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    full_name = serializers.ReadOnlyField()
    time_offline = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'full_name', 'email', 'created_at', 'is_online', 'last_seen', 'time_offline')
    
    def get_time_offline(self, obj):
        return obj.get_time_offline()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError('Credenciais inválidas.')
            if not user.is_active:
                raise serializers.ValidationError('Usuário desativado.')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Email e senha são obrigatórios.')


class LoginResponseSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    full_name = serializers.ReadOnlyField()
    access_token = serializers.SerializerMethodField()
    refresh_token = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'full_name', 'email', 'access_token', 'refresh_token')
        
    def get_access_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return str(refresh.access_token)
        
    def get_refresh_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return str(refresh)


class UserMeSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    full_name = serializers.ReadOnlyField()
    time_offline = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'full_name', 'email', 'created_at', 'is_online', 'last_seen', 'last_login_time', 'time_offline')
    
    def get_time_offline(self, obj):
        return obj.get_time_offline()
