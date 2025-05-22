from django.db import models
from django.contrib.auth import get_user_model

from core.apps.common.models import TimedBaseModel
from core.apps.projects.models import ProjectService
from core.apps.baskets.managers import BasketManager

User = get_user_model()



class Basket(TimedBaseModel):
    user = models.ForeignKey(
        to = User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Пользователь"
        )
    project_service = models.ForeignKey(
        to = ProjectService,
        on_delete=models.CASCADE,
        verbose_name="Услуга"
        )
    session_key = models.CharField(
        max_length=128,
        verbose_name="Ключ сессии"
        )

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
        unique_together = [  
            ['user', 'project_service'],
            ['session_key', 'project_service']
        ]
        indexes = [
        models.Index(fields=['user', 'session_key']),
        models.Index(fields=['project_service']),
    ]
        
    objects = BasketManager()
    raw_objects = models.Manager()

    def __str__(self) -> str:
        parts = []
        if self.user:
            parts.append(f"Пользователь: {self.user.username}")
        if self.session_key:
            parts.append(f"Сессия: {self.session_key[:10]}...")
        parts.append(f"Услуга: {self.project_service.service.title}")
        return " | ".join(parts)
    
    @property
    def price(self):
        """Цена через связанный проект-услугу"""
        return self.project_service.get_price()