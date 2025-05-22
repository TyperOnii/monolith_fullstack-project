from rest_framework import serializers
from core.apps.users.models import Admin

class AdminProfileShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Admin
        fields = (
            'created_at',
            'updated_at',
            )


class AdminProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        #TODO: изменить
        fields = ('created_at', 'updated_at',)