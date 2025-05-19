from django.db import models

from core.apps.common.utils import (get_path_upload_project_images,
                                    validate_size_image)

from .projects import Project


class ProjectImage(models.Model):
    #при удалении проекта, добавить удалении картинок
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name="project_images")
    image = models.ImageField(upload_to = get_path_upload_project_images, verbose_name="Изображение дома", validators=[validate_size_image])

    def __str__(self):
        return f"Изображение проекта {self.project.title}"
    
    class Meta:
        verbose_name = "Изображения проекта"
        verbose_name_plural = "Изображения проектов"