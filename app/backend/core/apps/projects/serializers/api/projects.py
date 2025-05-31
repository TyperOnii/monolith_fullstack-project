from crum import get_current_user
from rest_framework.exceptions import ParseError
from rest_framework import serializers

from core.apps.common.serializers import ExtendedModelsSerializer
from core.apps.projects.models.projects import Project
from core.apps.projects.serializers.api.project_specifications import ProjectSpecificationsSerializer
from core.apps.projects.serializers.api.project_images import ProjectImagesListSerializer

#TODO Добавить миксин для наследования всех сериализаторов проектов


class ProjectSearchListSerializer(ExtendedModelsSerializer):
    project_specifications = ProjectSpecificationsSerializer()
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'project_specifications', 'main_image')

    def get_main_image(self, obj):
        first_image = obj.project_images.first()
        if first_image:
            return ProjectImagesListSerializer(first_image).data
        return None
    
class ProjectListSerializer(ExtendedModelsSerializer):
    project_specifications = ProjectSpecificationsSerializer()
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'title', 'description',  'is_visible', 'project_specifications', 'main_image')

    def get_main_image(self, obj):
        first_image = obj.project_images.first()
        if first_image:
            return ProjectImagesListSerializer(first_image).data
        return None

class ProjectRetrieveSerializer(ExtendedModelsSerializer):
    project_images = ProjectImagesListSerializer(many=True)
    project_specifications = ProjectSpecificationsSerializer()

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'is_visible', 'project_images', 'project_specifications')

    

class ProjectCreateSerializer(ExtendedModelsSerializer):
    project_images = ProjectImagesListSerializer(many=True)
    project_specifications = ProjectSpecificationsSerializer()

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'is_visible', 'project_images', 'project_specifications')

    def validate(self, attrs):
        if attrs.get('is_visible', False):
            project = Project.objects.get(id=attrs.get('id'))
            project.update_visibility()
            if not project.is_visible:
                #TODO: добавить функцию в project для того что бы узнать что не заполненно
                # и вывести соответствующее сообщение. Так же для админа выводить список не заполенных обязательных полей
                raise serializers.ValidationError(
                    'Проект не может быть виден: заполните все обязательные поля'
                )


class ProjectUpdateSerializer(ExtendedModelsSerializer):
    project_images = ProjectImagesListSerializer(many=True)
    project_specifications = ProjectSpecificationsSerializer()
    

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'is_visible', 'project_images', 'project_specifications')
    
    def validate(self, attrs):
        if attrs.get('is_visible', False):
            project = Project.objects.get(id=attrs.get('id'))
            project.update_visibility()
            if not project.is_visible:
                #TODO: добавить функцию в project для того что бы узнать что не заполненно
                # и вывести соответствующее сообщение. Так же для админа выводить список не заполенных обязательных полей
                raise serializers.ValidationError(
                    'Проект не может быть виден: заполните все обязательные поля'
                )


class ProjectDestroySerializer(ExtendedModelsSerializer):

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'is_visible')