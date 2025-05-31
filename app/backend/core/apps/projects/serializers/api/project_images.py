from core.apps.common.serializers import ExtendedModelsSerializer
from core.apps.projects.models.project_images import ProjectImage


class ProjectImagesListSerializer(ExtendedModelsSerializer):
    class Meta:
        model = ProjectImage
        fields = ['id', 'image']


class ProjectImagesCDSerializer(ExtendedModelsSerializer):
    class Meta:
        model = ProjectImage
        fields = ['id', 'image', 'project']