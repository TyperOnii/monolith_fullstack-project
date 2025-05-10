from django.db import models
from django.forms import ValidationError
from django.utils.text import slugify
from core.apps.common.utils import unique_slugify

class ProjectCategory(models.Model):
    floor = models.PositiveIntegerField(blank=True, null=True, verbose_name='Этажность' )
    slug = models.SlugField(max_length=230, unique=True, blank=True, null=True, verbose_name="URL")
    the_area_filter = models.PositiveIntegerField(blank=True, null=True, verbose_name="Начниается от скольки метров в квадрате")
    price_filter = models.DecimalField(blank=True, null=True, max_digits = 15, decimal_places=0, verbose_name="Начиная от какой суммы")

    def clean(self):
        if not any([self.floor, self.the_area_filter, self.price_filter]):
            raise ValidationError("Хотя бы одно поле фильтрации должно быть заполнено!")
    
    def save(self, *args, **kwargs):
        slug = slugify(f"category-{self.floor}-{self.the_area_filter}-{self.price_filter}")
        self.slug = unique_slugify(self, slug)
        super().save(*args, **kwargs)
    

    def __str__(self):
        parts = []
        if self.floor is not None:
            parts.append(f"по этажности от {self.floor}")
        if self.the_area_filter is not None:
            parts.append(f"от {self.the_area_filter} м²")
        if self.price_filter is not None:
            parts.append(f"по цене от {self.price_filter} руб.")
    
        if not parts:
            return "Категория без фильтров"
    
        return "Категория фильтрует проекты " + ", ".join(parts)
    

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
