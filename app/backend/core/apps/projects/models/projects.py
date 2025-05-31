from django.db import models

from core.apps.common.models import TimedBaseModel
from core.apps.projects.models.project_specifications import ProjectSpecifications

class Project(TimedBaseModel):

    REQUIRED_VISIBILITY_FIELDS = ['title', 'description']

    #TODO: при сохранении моделей которые расширяют проекты, нужно делать проверку, заполнились ли все обязательные поля, и только если да, менять is_visible на True
    title = models.CharField(
        max_length=255,
        verbose_name="Название проекта",
        )
    description = models.TextField(
        blank=True,
        default='',
        verbose_name='Описание проекта'
        )
    
    services = models.ManyToManyField(
        'Service',
        through='ProjectService',
        related_name='projects',
        verbose_name='Услуги в проекте',
        help_text='Услуги которые были добавлены для этого проекта'
    )
    is_visible = models.BooleanField(
        default=False,
        verbose_name = 'Виден ли проект в катологе'
        )
    #count_services = models.IntegerField(default=0,blank=True,verbose_name="Количество сервисов этого проекта, для видимости что покупатель выбрал все")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def get_count_services(self):
        # добавить логику для подсетча услуг в этом проекте
        return self.services.count()

    def update_visibility(self):
        """Обновляет статус видимости на основе заполненности полей"""
        # Проверяем обязательные поля в проекте
        for field in self.REQUIRED_VISIBILITY_FIELDS:
            value = getattr(self, field)
            if value is None or isinstance(value, str) and not value.strip():
                self.is_visible = False
                return
        
        # Проверяем обязательные поля в характеристиках
        try:
            specs = self.project_specifications
            if not specs.is_complete():
                self.is_visible = False
                return
        except ProjectSpecifications.DoesNotExist:
            self.is_visible = False
            return
        
        if not self.project_images.exists():
            self.is_visible = False
            return
        
        # Если все проверки пройдены
        self.is_visible = True

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)  
            ProjectSpecifications.objects.create(project=self)
            return  
        
        self.update_visibility()
        super().save(*args, **kwargs)

