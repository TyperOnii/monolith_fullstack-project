from django.db import models

from core.apps.common.utils import (get_path_upload_project_images,
                                    validate_size_image)

from .projects import Project


class ProjectImage(models.Model):
    #при удалении проекта, добавить удалении картинок
    #TODO: добавить возможность выбора главной фотографии
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name="project_images"
        )
    image = models.ImageField(
        upload_to = get_path_upload_project_images,
        verbose_name="Изображение дома",
        validators=[validate_size_image]
        )

    def __str__(self):
        return f"Изображение проекта {self.project.title}"
    
    class Meta:
        verbose_name = "Изображения проекта"
        verbose_name_plural = "Изображения проектов"


    def save(self, *args, **kwargs):
        """
        При сохранении изображения обновляем видимость проекта
        """
        super().save(*args, **kwargs)
        self.project.update_visibility()
        self.project.save(update_fields=['is_visible'])
    
    def delete(self, *args, **kwargs):
        """
        При удалении изображения обновляем видимость проекта
        """
        project = self.project
        super().delete(*args, **kwargs)
        project.update_visibility()
        project.save(update_fields=['is_visible'])