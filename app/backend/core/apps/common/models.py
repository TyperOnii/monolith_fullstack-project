from django.db import models
from django.conf import settings


class TimedBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name= 'Дата обновления')

    class Meta:
        abstract = True


class InfoMixin(TimedBaseModel):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='created_%(app_label)s_%(class)s',
        verbose_name='Создатель',
        null=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='updated_%(app_label)s_%(class)s',
        verbose_name='Обновил',
        null=True
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        from crum import get_current_user

        user = get_current_user()

        if user and not user.pk:
            user = None

        if not self.pk:
            self.created_by = user
        self.updated_by = user
        super().save(*args, **kwargs)