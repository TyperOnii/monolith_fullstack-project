from django.db import models
from .user import User
from core.apps.common.models import TimedBaseModel

class Admin(TimedBaseModel):
    user = models.OneToOneField(to = User, on_delete=models.CASCADE, related_name="admin_user")


    class Meta:
        verbose_name = "Админ"
        verbose_name_plural = "Админы"
    
    def __str__(self):
        return self.user.username
