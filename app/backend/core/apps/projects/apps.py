from django.apps import AppConfig


class ProjectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.apps.projects'
    verbose_name = 'Проекты'

    def ready(self):
        import core.apps.projects.signals