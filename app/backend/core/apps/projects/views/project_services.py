from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema, extend_schema_view

from core.apps.common.views.mixins import CRUDViewSet
from core.apps.projects.models.project_services import ProjectService
from core.apps.projects.serializers.api import project_services as project_service_serializers
from core.apps.common.description import get_description
from core.apps.projects.filters import ProjectServiceFilter


class ProjectServiceView(CRUDViewSet):
    queryset = ProjectService.objects.all()
    serializer_class = project_service_serializers.ProjectServiceListSerializer
    permission_classes = [AllowAny]
    multi_permission_classes = {
        'list': [AllowAny],
        'create': [AllowAny],
        'update': [AllowAny],
        'partial_update': [AllowAny],
        'retrieve': [AllowAny],
        'destroy': [AllowAny],
    }
    multi_serializer_classes = {
        'list': project_service_serializers.ProjectServiceListSerializer,
        'create': project_service_serializers.ProjectServiceCreateSerializer,
        'update': project_service_serializers.ProjectServiceUpdateSerializer,
        'partial_update': project_service_serializers.ProjectServiceUpdateSerializer,
        'retrieve': project_service_serializers.ProjectServiceRetrieveSerializer,
        'destroy': project_service_serializers.ProjectServiceDestroySerializer,
    }
    http_method_names = ['get', 'post', 'patch', 'delete']

    filter_backends = [
        OrderingFilter,
        SearchFilter,
        DjangoFilterBackend,
    ]
    ordering_fields = ['price',]
    search_fields = ['price',]
    filterset_class = ProjectServiceFilter

project_service_schema = extend_schema_view(
    list = extend_schema(
        summary='Список услуг проекта',
        description=get_description(
            action='list', 
            view=ProjectServiceView
        ),
        tags=['projects'],
    ),
    create = extend_schema(
        summary='Создание услуги проекта',
        description=get_description(
            action='create', 
            view=ProjectServiceView
        ),
        tags=['projects-manage'],
    ),
    destroy = extend_schema(
        summary='Удаление услуги проекта',
        description=get_description(
            action='destroy', 
            view=ProjectServiceView
        ),
        tags=['projects-manage'],
    ),
    update = extend_schema(
        summary='Обновление услуги проекта',
        description=get_description(
            action='update', 
            view=ProjectServiceView
        ),
        tags=['projects-manage'],
    ),
    partial_update = extend_schema(
        summary='Частичное обновление услуги проекта',
        description=get_description(
            action='partial_update', 
            view=ProjectServiceView
        ),
        tags=['projects-manage'],
    ),
    retrieve = extend_schema(
        summary='Получение услуги проекта',
        description=get_description(
            action='retrieve', 
            view=ProjectServiceView
        ),
        tags=['projects'],
    ),
)

project_service_schema = project_service_schema(
    ProjectServiceView
)