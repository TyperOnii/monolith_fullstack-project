from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.exceptions import ParseError
from rest_framework import serializers
from django.conf import settings

from core.apps.users.models import  Admin, Client
from core.apps.users.serializers.api.mixins import ProfileSerializerMixin, ProfileUpdateMixin


User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
            'phone_number',
            'role',
        )
    
    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise ParseError('Пользователь с таким email уже существует')
        return email
    
    def validate_phone_number(self, value):
        phone_number = value
        if User.objects.filter(phone_number=phone_number).exists():
            raise ParseError('Пользователь с таким номером телефона уже существует')
        return phone_number
    
    def validate_password(self, value):
        validate_password(value)
        return value
    
    def create(self, validated_data):
        request = self.context.get('request')
        role = validated_data.get('role')
        if role == 'admin':

            if not request.data.get('secret_key'):
                raise ParseError('Для создания администратора необходимо указать secret_key')
            #TODO: def chech_secret_key(self, value):
            if request.data.get('secret_key') != settings.ADMIN_SECRET_KEY:
                raise ParseError('Неверный Secret_key')
            
            user = User.objects.create_user(**validated_data)
            Admin.objects.create(user=user)
        elif role == 'client':
            user = User.objects.create_user(**validated_data)
            Client.objects.create(user=user)


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
#            'username',
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
#            'username',
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


