from core.apps.projects.models.project_services import ProjectService
from core.apps.common.serializers import ExtendedModelsSerializer


class ProjectServiceNestedSerializer(ExtendedModelsSerializer):

    class Meta:
        model = ProjectService
        fields = ['id', 'service', 'price', 'download_link',]