import os
from drf_spectacular.utils import extend_schema, extend_schema_view

from core.apps.common.views.mixins import CDViewSet
from core.apps.projects.models.project_images import ProjectImage
from core.apps.projects.serializers.api.project_images import ProjectImagesCDSerializer

@extend_schema_view(
    create=extend_schema(
        summary='Создание изображения проекта',
        description='Создание изображения проекта',
        tags=['projects'],
        ),
    destroy=extend_schema(
        summary='Создание изображения проекта',
        description='Создание изображения проекта',
        tags=['projects'],
    )
    )
class ProjectImagesView(CDViewSet):
    queryset = ProjectImage.objects.all()
    serializer_class = ProjectImagesCDSerializer
    #TODO: permission admin

    def perform_destroy(self, instance):
        if instance.image and os.path.isfile(instance.image.path):
            os.remove(instance.image.path)  
        super().perform_destroy(instance)