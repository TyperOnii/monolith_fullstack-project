from rest_framework import serializers
from core.apps.users.models import Client

class ClientProfileShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = (
            'recommendation_status',
            )
        
class ClientProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('recommendation_status', 'city')
        extra_kwargs = {
            'recommendation_status': {'required': False},
            'city': {'required': False}
        }