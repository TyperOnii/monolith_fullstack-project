from django.db import models

from core.apps.common.models import TimedBaseModel

from .user import User


class Admin(TimedBaseModel):
    #TODO: сделать primary key
    user = models.OneToOneField(
        to = User,
        on_delete=models.CASCADE,
        related_name="admin_user"
        )


    class Meta:
        verbose_name = "Админ"
        verbose_name_plural = "Админы"
    
    def __str__(self):
        return self.user.username
