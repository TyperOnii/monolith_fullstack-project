from django.db import models

from core.apps.common.models import TimedBaseModel


class Project(TimedBaseModel):
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


