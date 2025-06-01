from rest_framework import serializers

from core.apps.baskets.models import Basket
from core.apps.projects.serializers.nested.project_services import ProjectServiceNestedSerializer

class BasketListSerializer(serializers.ModelSerializer):
    project_service = ProjectServiceNestedSerializer(read_only=True)
    price = serializers.SerializerMethodField()

    class Meta:
        model = Basket
        fields = ('id', 'project_service', 'created_at', 'price')
    
    def get_price(self, obj):
        return obj.price

class BasketAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = ('project_service',)
        extra_kwargs = {
            'project_service': {'required': True}
        }

    def validate(self, attrs):
     user = self.context['request'].user
     session_key = self.context['request'].session.session_key
     project_service = attrs['project_service']

     # Проверяем, не существует ли уже такой записи
     if Basket.objects.filter(
         user=user if user.is_authenticated else None,
         session_key=session_key,
         project_service=project_service
     ).exists():
         raise serializers.ValidationError(
             "Эта услуга уже добавлена в корзину"
         )
     
     return attrs

class BasketMergeSerializer(serializers.Serializer):
    session_key = serializers.CharField(max_length=128, required=True)