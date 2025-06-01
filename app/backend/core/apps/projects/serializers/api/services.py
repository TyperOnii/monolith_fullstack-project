from rest_framework import serializers

from core.apps.projects.models.project_services import Service
from core.apps.common.serializers import ExtendedModelsSerializer


class ProjectServiceListSerializer(ExtendedModelsSerializer):
    class Meta:
        model = Service
        fields = '__all__'



class ProjectServiceCreateSerializer(ExtendedModelsSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Service
        fields = ['id', 'title', 'description',]



class ProjectServiceUpdateSerializer(ExtendedModelsSerializer):
    class Meta:
        model = Service
        fields = ['title', 'description',]


class ProjectServiceDestroySerializer(ExtendedModelsSerializer):
    class Meta:
        model = Service
        fields = ['id',]



class ProjectServiceRetrieveSerializer(ExtendedModelsSerializer):
    class Meta:
        model = Service
        fields = '__all__'


