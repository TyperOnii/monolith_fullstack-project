from core.apps.common.serializers import ExtendedModelsSerializer

from core.apps.projects.models.projects import Project

class ProjectListSerializer(ExtendedModelsSerializer):

    class Meta:
        model = Project
        fields = ('id', 'title', 'description',  'is_visible')