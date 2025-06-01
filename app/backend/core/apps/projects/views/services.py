from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema, extend_schema_view

from core.apps.common.views.mixins import ListViewSet, CRUDViewSet
from core.apps.projects.models.project_services import Service
from core.apps.projects.serializers.api import services as project_service_serializers
from core.apps.common.description import get_description




class ServiceView(CRUDViewSet):
    queryset = Service.objects.all()
    serializer_class = project_service_serializers.ProjectServiceListSerializer
    permission_classes = [AllowAny]
    #TODO: Настроить разрешения
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
        #MyProjectBackend,
    ]

    ordering_fields = ['title','id',]
    search_fields = ['title',]
    #filterset_class = ProjectServiceFilter



project_service_schema = extend_schema_view(
    list = extend_schema(
        summary='Список возможных услуг',
        description=get_description(
            action='list', 
            view=ServiceView
        ),
        tags=['projects',],
    ),
    create = extend_schema(
        summary='Создание возможных услуг',
        description=get_description(
            action='create', 
            view=ServiceView
        ),
        tags=['administration'],
    ),
    destroy = extend_schema(
        summary='Удаление возможных услуг',
        description=get_description(
            action='destroy', 
            view=ServiceView
        ),
        tags=['administration'],
    ),
    update = extend_schema(
        summary='Обновление возможных услуг',
        description=get_description(
            action='update', 
            view=ServiceView
        ),
        tags=['administration'],
    ),
    partial_update = extend_schema(
        summary='Частичное обновление возможных услуг',
        description=get_description(
            action='partial_update', 
            view=ServiceView
        ),
        tags=['administration'],
    ),
    retrieve = extend_schema(
        summary='Получение возможной услуги',
        description=get_description(
            action='retrieve', 
            view=ServiceView
        ),
        tags=['projects'],
    ),

)

project_service_schema = project_service_schema(
    ServiceView
)