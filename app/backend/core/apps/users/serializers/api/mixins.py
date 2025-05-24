from rest_framework import serializers


from core.apps.users.serializers.nested.admin_profile import AdminProfileShortSerializer, AdminProfileUpdateSerializer
from core.apps.users.serializers.nested.client_profile import ClientProfileShortSerializer, ClientProfileUpdateSerializer

class ProfileSerializerMixin:

    USER_RELATION_NAME_MAPPING = {'admin': 'admin_user', 'client': 'client_user'}

    def get_profile_serializer(self, obj):

        profile_mapping = {
            'admin': (AdminProfileShortSerializer, self.USER_RELATION_NAME_MAPPING['admin']),
            'client': (ClientProfileShortSerializer, self.USER_RELATION_NAME_MAPPING['admin']),
        }
        
        serializer_class, profile_attr = profile_mapping.get(obj.role, (None, None))
        
        if not serializer_class or not hasattr(obj, profile_attr):
            return None
        
        profile = getattr(obj, profile_attr)
        return serializer_class(profile, context=self.context).data

class ProfileUpdateMixin:

    USER_RELATION_NAME_MAPPING = {'admin': 'admin_user', 'client': 'client_user'}

    def get_profile_serializer(self, instance):
        role = instance.role
        profile_mapping = {
            'admin': (AdminProfileUpdateSerializer, self.USER_RELATION_NAME_MAPPING['admin']),
            'client': (ClientProfileUpdateSerializer, self.USER_RELATION_NAME_MAPPING['admin']),
        }
        serializer_class, profile_attr = profile_mapping.get(role, (None, None))
        
        if not serializer_class or not hasattr(instance, profile_attr):
            raise serializers.ValidationError(
                {'profile': f'Профиль для роли {role} не найден'}
            )
            
        return serializer_class(getattr(instance, profile_attr))