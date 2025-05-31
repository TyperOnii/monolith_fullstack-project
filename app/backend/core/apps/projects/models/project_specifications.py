from django.db import models



class ProjectSpecifications(models.Model):

    REQUIRED_VISIBILITY_FIELDS = [
        'floors', 'overall_length', 'overall_width', 'area',
        'wall_material', 'overlap', 'roof_type', 'roofing_material',
        'exterior_decoration', 'foundation'
    ]

    project = models.OneToOneField(
        to = "projects.Project",
        on_delete=models.CASCADE,
        related_name = "project_specifications",
        verbose_name="Проект"
        )
    floors = models.PositiveIntegerField(
        verbose_name="Этажность",
        blank=True,
        null=True,
        )
    overall_length = models.FloatField(
        verbose_name="Длина",
        blank=True,
        null=True,
        )
    overall_width = models.FloatField(
        verbose_name="Ширина",
        blank=True,
        null=True,
        )
    area = models.PositiveIntegerField(
        verbose_name="Площадь",
        blank=True,
        null=True,
        )
    construction_cost = models.DecimalField(
        max_digits=20, 
        decimal_places=2,
        verbose_name="Стоимость строительства от",
        blank=True,
        null=True,
        )


    wall_material = models.CharField(
        max_length=1024,
        verbose_name="Материал стен",
        blank=True,
        null=True,
        )
    overlap = models.CharField(
        max_length=1024,
        verbose_name="Перекрытие",
        blank=True,
        null=True,
        )
    roof_type = models.CharField(
        max_length=1024,
        verbose_name="Тип кровли",
        blank=True,
        null=True,
        )
    roofing_material = models.CharField(
        max_length=1024,
        verbose_name="Кровельный материал",
        blank=True,
        null=True,
        )
    exterior_decoration = models.CharField(
        max_length=1024,
        verbose_name="Наружная отделка",
        blank=True,
        null=True,
        )
    foundation = models.CharField(
        max_length=1024,
        verbose_name = "Фундамент",
        blank=True,
        null=True,
        )


    def is_complete(self):
        """Проверяет, заполнены ли все обязательные для видимости поля"""
        for field in self.REQUIRED_VISIBILITY_FIELDS:
            value = getattr(self, field)
            if value is None or isinstance(value, str) and not value.strip():
                return False
        return True

    def save(self, *args, **kwargs):
        if self.is_complete():
            self.project.is_visible = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Характеристики проекта {self.project.title}"
    
    class Meta:
        verbose_name = "Характеристики проекта"
        verbose_name_plural = "Характеристики проектов"

    