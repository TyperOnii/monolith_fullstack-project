from rest_framework import serializers
from core.apps.users.models import Client, ReferralCode

class ReferralCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralCode
        fields = ('code', 'discount', 'active', 'uses_count')

class ClientProfileShortSerializer(serializers.ModelSerializer):

    referral_code = ReferralCodeSerializer(read_only=True)


    class Meta:
        model = Client
        fields = (
            'recommendation_status',
            'project_completion_percentage',
            'city',
            'referral_code',
            )
        
class ClientProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('recommendation_status', 'city')
        extra_kwargs = {
            'recommendation_status': {'required': False},
            'city': {'required': False}
        }

