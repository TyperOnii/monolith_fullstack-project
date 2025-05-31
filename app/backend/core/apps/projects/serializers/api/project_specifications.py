from core.apps.common.serializers import ExtendedModelsSerializer
from core.apps.projects.models.project_specifications import ProjectSpecifications

class ProjectSpecificationsSerializer(ExtendedModelsSerializer):
    class Meta:
        model = ProjectSpecifications
        exclude = ('project', 'id')