from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Count, Case, When, Value, BooleanField

from core.apps.common.views.mixins import ListViewSet, CRUDViewSet
from core.apps.projects.models.projects import Project
from core.apps.projects.serializers.api import projects as project_serializers
from core.apps.projects.filters import ProjectFilter
from core.apps.projects.backends import MyProjectBackend



@extend_schema_view(
    list=extend_schema(
        summary='Список проектов для просмотра в каталоге',
        description='Список проектов для просмотра в каталоге',
        tags=['projects'],
        )
    )
class ProjectSearchListView(ListViewSet):
    queryset = Project.objects.filter(is_visible=True)
    serializer_class = project_serializers.ProjectSearchListSerializer


@extend_schema_view(
    list=extend_schema(
        summary='Список проектов',
        description='Список проектов',
        tags=['projects'],
    ),
    create=extend_schema(
        summary='Создание проекта',
        description='Создание проекта',
        tags=['projects'],
    ),
    update=extend_schema(
        summary='Обновление проекта',
        description='Обновление проекта',
        tags=['projects'],
    ),
    partial_update=extend_schema(
        summary='Частичное обновление проекта',
        description='Частичное обновление проекта',
        tags=['projects'],
    ),
    retrieve=extend_schema(
        summary='Получение проекта',
        description='Получение проекта',
        tags=['projects'],
    ),
    destroy=extend_schema(
        summary='Удаление проекта',
        description='Удаление проекта',
        tags=['projects'],
    )
)
class ProjectView(CRUDViewSet):
    queryset = Project.objects.all()
    serializer_class = project_serializers.ProjectListSerializer
    permission_classes = [AllowAny]
    # Настроить разрешения
    multi_permission_classes = {
        'list': [AllowAny],
        'create': [AllowAny],
        'update': [AllowAny],
        'partial_update': [AllowAny],
        'retrieve': [AllowAny],
        'destroy': [AllowAny],
    }

    multi_serializer_classes = {
        #'admin_list': project_serializers.ProjectListSerializer,
        #'client_list': project_serializers.ProjectListSerializer,
        'list': project_serializers.ProjectListSerializer,
        'create': project_serializers.ProjectCreateSerializer,
        'update': project_serializers.ProjectUpdateSerializer,
        'partial_update': project_serializers.ProjectUpdateSerializer,
        'retrieve': project_serializers.ProjectRetrieveSerializer,
        'destroy': project_serializers.ProjectDestroySerializer,
    }

    http_method_names = ['get', 'post', 'patch', 'delete']

    filter_backends = [
        OrderingFilter,
        SearchFilter,
        DjangoFilterBackend,
        #MyProjectBackend,
    ]

    ordering_fields = ['title','id',]
    search_fields = ['title',]
    filterset_class = ProjectFilter

    def get_queryset(self):
        user = self.request.user
        queryset = Project.objects.prefetch_related(
            'services',
            'project_specifications',
            'project_images',
        ).annotate(
            count_services=Count('services'),
            # can_manage=Case(
            #     When(created_by=user, then=Value(True)),  
            #     default=Value(False),
            #     output_field=BooleanField()
            # )
        )

        return queryset