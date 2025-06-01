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
from core.apps.common.description import get_description


#TODO: Подумать нужно ли это представление? Либо убрать list в ProjectView
class ProjectSearchListView(ListViewSet):
    queryset = Project.objects.filter(is_visible=True)
    serializer_class = project_serializers.ProjectSearchListSerializer



class ProjectView(CRUDViewSet):
    queryset = Project.objects.all()
    serializer_class = project_serializers.ProjectListSerializer
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
        #TODO: вынести в Factory
        #TODO Prefetch('services', queryset=Service.objects.only('id', 'name'))
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
        # if user.role == 'client':
        #     queryset = queryset.filter(is_visible=True)

        return queryset


project_model_schema = extend_schema_view(
    list=extend_schema(
        summary='Список проектов',
        description=get_description(
            action='list', 
            view=ProjectView
        ),
        tags=['projects'],
        ),
    create=extend_schema(
        summary='Создание проекта',
        description=get_description(
            action='create', 
            view=ProjectView
        ),
        tags=['projects-manage'],
        ),
    update=extend_schema(
        summary='Обновление проекта',
        description=get_description(
            action='update', 
            view=ProjectView
        ),
        tags=['projects-manage'],
        ),
    destroy=extend_schema(
        summary='Удаление проекта',
        description=get_description(
            action='destroy', 
            view=ProjectView
        ),
        tags=['projects-manage'],
        ),
    retrieve=extend_schema(
        summary='Просмотр проекта',
        description=get_description(
            action='retrieve', 
            view=ProjectView
        ),
        tags=['projects'],
        ),
    partial_update=extend_schema(
        summary='Частичное обновление проекта',
        description=get_description(
            action='partial_update', 
            view=ProjectView
        ),
        tags=['projects-manage'],
    )
)

project_search_list_schema = extend_schema_view(
    list=extend_schema(
        summary='Список проектов для просмотра в каталоге',
        description=get_description(
            action='list', 
            view=ProjectSearchListView
        ),
        tags=['projects'],
        )
    )

project_search_list_schema = project_search_list_schema(ProjectSearchListView)
ProjectView_schema = project_model_schema(ProjectView)