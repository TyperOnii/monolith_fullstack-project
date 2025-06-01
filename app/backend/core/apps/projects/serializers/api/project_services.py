from rest_framework import serializers

from core.apps.projects.models.project_services import ProjectService
from core.apps.common.serializers import ExtendedModelsSerializer


class ProjectServiceListSerializer(ExtendedModelsSerializer):

    class Meta:
        model = ProjectService
        fields = ['id', 'project', 'service', 'price', 'download_link',]


class ProjectServiceCreateSerializer(ExtendedModelsSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = ProjectService
        fields = ['id', 'project', 'service', 'price', 'download_link',]


class ProjectServiceDestroySerializer(ExtendedModelsSerializer):

    class Meta:
        model = ProjectService
        fields = ['id',]


class ProjectServiceRetrieveSerializer(ExtendedModelsSerializer):

    class Meta:
        model = ProjectService
        fields = ['id','project', 'service', 'price', 'download_link',]


class ProjectServiceUpdateSerializer(ExtendedModelsSerializer):

    class Meta:
        model = ProjectService
        fields = ['price', 'download_link',]

    
#TODO сделать еще для отображения в ProjectSerualizer