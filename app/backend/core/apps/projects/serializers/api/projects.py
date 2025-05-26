from crum import get_current_user
from rest_framework.exceptions import ParseError

from core.apps.common.serializers import ExtendedModelsSerializer
from core.apps.projects.models.projects import Project

class ProjectSearchListSerializer(ExtendedModelsSerializer):

    class Meta:
        model = Project
        fields = ('id', 'title', 'description',)

class ProjectListSerializer(ExtendedModelsSerializer):

    class Meta:
        model = Project
        fields = ('id', 'title', 'description',  'is_visible')

class ProjectRetrieveSerializer(ExtendedModelsSerializer):

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'is_visible')


class ProjectCreateSerializer(ExtendedModelsSerializer):

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'is_visible')

    def validate(self, attrs):
        current_user = get_current_user()

        user_role = current_user.role
        if user_role != 'admin':
            raise ParseError('Только администратор может создавать проекты')
        

        return super().validate(attrs)


class ProjectUpdateSerializer(ExtendedModelsSerializer):

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'is_visible')


class ProjectDestroySerializer(ExtendedModelsSerializer):

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'is_visible')