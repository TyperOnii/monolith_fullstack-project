import os
from drf_spectacular.utils import extend_schema, extend_schema_view

from core.apps.common.permissions import IsAdmin
from core.apps.common.views.mixins import CDViewSet
from core.apps.projects.models.project_images import ProjectImage
from core.apps.projects.serializers.api.project_images import ProjectImagesCDSerializer
from core.apps.common.description import get_description


class ProjectImagesView(CDViewSet):
    queryset = ProjectImage.objects.all()
    serializer_class = ProjectImagesCDSerializer
    permission_classes = (IsAdmin,)

    def perform_destroy(self, instance):
        if instance.image and os.path.isfile(instance.image.path):
            os.remove(instance.image.path)  
        super().perform_destroy(instance)



#TODO: вынести в отдельный файл docs.py
create_schema = extend_schema(
    summary='Создание изображения проекта',
    description=get_description(
        action='create', 
        view=ProjectImagesView  
    ),
    tags=['projects-manage'],
)(ProjectImagesView.create)

destroy_schema = extend_schema(
    summary='Удаление изображения проекта',
    description=get_description(
        action='destroy', 
        view=ProjectImagesView
    ),
    tags=['projects-manage'],
)(ProjectImagesView.destroy)


ProjectImagesView.create = create_schema
ProjectImagesView.destroy = destroy_schema