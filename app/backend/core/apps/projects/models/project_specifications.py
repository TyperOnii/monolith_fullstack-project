from django.db import models

from .projects import Project


class Project_Specifications(models.Model):
    project = models.OneToOneField(to = Project, on_delete=models.CASCADE, related_name = "project_specifications", verbose_name="Проект")
    floors = models.PositiveIntegerField(verbose_name="Этажность")
    overall_length = models.FloatField(verbose_name="Длина")
    overall_width = models.FloatField(verbose_name="Ширина")
    area = models.PositiveIntegerField(default = 0, verbose_name="Площадь")
    construction_cost = models.DecimalField(default= 0.00, max_digits=20,decimal_places=2,verbose_name="Стоимость строительства от")


    wall_material = models.CharField(max_length=1024, verbose_name="Материал стен")
    overlap = models.CharField(max_length=1024, verbose_name="Перекрытие")
    roof_type = models.CharField(max_length=1024, verbose_name="Тип кровли")
    roofing_material = models.CharField(max_length=1024, verbose_name="Кровельный материал")
    exterior_decoration = models.CharField(max_length=1024, verbose_name="Наружная отделка")
    foundation = models.CharField(max_length=1024, verbose_name = "Фундамент", blank=True, default='')


    def __str__(self):
        return f"Характеристики проекта {self.project.title}"
    
    class Meta:
        verbose_name = "Характеристики проекта"
        verbose_name = "Характеристики проектов"