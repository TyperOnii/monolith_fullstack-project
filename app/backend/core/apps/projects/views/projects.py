from drf_spectacular.utils import extend_schema, extend_schema_view

from core.apps.common.views.mixins import ListViewSet
from core.apps.projects.models.projects import Project
from core.apps.projects.serializers.api.projects import ProjectListSerializer


@extend_schema_view(
    list=extend_schema(
        summary='Список проектов',
        description='Список проектов',
        tags=['projects'],
        )
    )
class ProjectListViewSet(ListViewSet):
    queryset = Project.objects.filter(is_visible=True)
    serializer_class = ProjectListSerializer