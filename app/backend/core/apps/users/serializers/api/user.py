from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.exceptions import ParseError
from rest_framework import serializers

from core.apps.users.serializers.nested.admin_profile import AdminProfileShortSerializer, AdminProfileUpdateSerializer
from core.apps.users.serializers.nested.client_profile import ClientProfileShortSerializer, ClientProfileUpdateSerializer
from core.apps.users.models import  Admin, Client



User = get_user_model()


class ProfileSerializerMixin:
    def get_profile_serializer(self, obj):
        profile_mapping = {
            'admin': (AdminProfileShortSerializer, 'admin_user'),
            'client': (ClientProfileShortSerializer, 'client_user'),
        }
        
        serializer_class, profile_attr = profile_mapping.get(obj.role, (None, None))
        
        if not serializer_class or not hasattr(obj, profile_attr):
            return None
        
        profile = getattr(obj, profile_attr)
        return serializer_class(profile, context=self.context).data

class ProfileUpdateMixin:
    def get_profile_serializer(self, instance):
        role = instance.role
        profile_mapping = {
            'admin': (AdminProfileUpdateSerializer, 'admin_user'),
            'client': (ClientProfileUpdateSerializer, 'client_user'),
        }
        serializer_class, profile_attr = profile_mapping.get(role, (None, None))
        
        if not serializer_class or not hasattr(instance, profile_attr):
            raise serializers.ValidationError(
                {'profile': f'Профиль для роли {role} не найден'}
            )
            
        return serializer_class(getattr(instance, profile_attr))

class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
        )
    
    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise ParseError('Пользователь с таким email уже существует')
        return email
    
    def validate_password(self, value):
        validate_password(value)
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)


        #user.refresh_from_db()
        #token = Token.objects.create(user=user)
        #token.confirm_email_ssend()
        return user
    
class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password')
    
    def validate(self, attrs):
        user = self.instance
        old_password = attrs.get('old_password')
        if not user.check_password(old_password):
            raise ParseError('Неверный старый пароль')
        return super().validate(attrs)
        
    def validate_new_password(self, value):
        validate_password(value)
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop('new_password')
        instance.set_password(password)
        instance.save()
        return instance


class MeSerializer(ProfileSerializerMixin, serializers.ModelSerializer):

    profile = serializers.SerializerMethodField()

    def get_profile(self, obj):
        return self.get_profile_serializer(obj)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'role',
            'email',
            'phone_number',
            'is_verified_phone',
            'is_verified_email',
            'profile',
        )
        read_only_fields = ('role', 'is_verified_phone', 'is_verified_email')

class MeUpdateSerializer(ProfileUpdateMixin, serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'profile',
        )
        extra_kwargs = {
            'email': {'required': False},
            'phone_number': {'required': False}
        }

    def get_profile(self, obj):
        return self.get_profile_serializer(obj).data

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        internal_value['profile_data'] = data.get('profile', {})
        return internal_value
    
    def validate(self, attrs):
        profile_data = attrs.get('profile_data', {})
    
        if profile_data:
            serializer = self.get_profile_serializer(self.instance)
            if not serializer:
                raise serializers.ValidationError(
                    {'profile': 'Профиль для вашей роли не найден'}
                )
            serializer.validate(profile_data)
    
        return attrs

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile_data', {})
        
        with transaction.atomic():
            # Создаем профиль, если его нет
            if instance.role == 'admin':
                if not hasattr(instance, 'admin_user'):
                    Admin.objects.create(user=instance)
            elif instance.role == 'client':
                if not hasattr(instance, 'client_user'):
                    Client.objects.create(user=instance)
        
            # Обновление основных полей пользователя
            instance = super().update(instance, validated_data)
        
            # Обновление профиля
            if profile_data:
                serializer = self.get_profile_serializer(instance)
                #TODO: проверить работает ли
                serializer.update(serializer.instance, profile_data)
            
        return instance


