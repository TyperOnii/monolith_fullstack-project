from django.db import models

from .projects import Project


class Service(models.Model):
    """
    Один из возможных услуг в составе проекта.
    Каждый проект имеет свой состав услуг.
    Какие услуги могут быть у проекта, регулируется админом, то есть экземпляры этой модели создаются админом.
    """
    title = models.CharField(max_length=1024, verbose_name="Название услуги")
    description = models.TextField(verbose_name = "Подробное описание")
    projects = models.ManyToManyField(
        Project,
        through='ProjectService',
        related_name='services',
        verbose_name="Связанные проекты",
        help_text="Проекты, в которых доступна эта услуга"
    )
    

    def __str__(self):
        return f"{self.title}"
    
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


class ProjectService(models.Model):
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE
        )
    service = models.ForeignKey(
        to=Service,
        on_delete=models.CASCADE
        )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена услуги"
        )
    download_link = models.URLField(
        blank=True,
        null=True,
        verbose_name="Ссылка на скачивание"
        )

    def __str__(self):
        return f"{self.service.title} для {self.project.title} "
    
    class Meta:
        unique_together = [['project','service']]
        verbose_name = "Услуга в проекте"
        verbose_name_plural = "Услуги в проекте"

    def get_price(self, discount=0):
        if discount:
            return self.price * (1 - discount)
        return self.price
