from django.db import models
from core.apps.common.models import TimedBaseModel


class Product(TimedBaseModel):
    title = models.CharField(max_length=255, verbose_name="Название товара", )
    description = models.TextField(blank=True, default='', verbose_name='Описание товара')
    is_visible = models.BooleanField(default=True, verbose_name = 'Виден ли товар в катологе')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

