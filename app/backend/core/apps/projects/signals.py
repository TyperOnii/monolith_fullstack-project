from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Project, ProjectImage

@receiver([post_save, post_delete], sender=ProjectImage)
def update_project_visibility_on_image_change(sender, instance, **kwargs):
    """
    Обновляет видимость проекта при добавлении или удалении изображений
    """
    try:
        project = instance.project
        project.update_visibility()
        project.save(update_fields=['is_visible'])
    except Project.DoesNotExist:
        pass