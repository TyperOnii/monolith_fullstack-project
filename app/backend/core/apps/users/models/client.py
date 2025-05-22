from django.db import models

from core.apps.common.models import TimedBaseModel

from .user import User


class Client(TimedBaseModel):
    # TODO: Добавить логику, повышения статуса клиента
    RECOMMENDATION_STATUS_CHOICES = [
        ('silver', 'Серебро'),
        ('gold', 'Золото'),
        ('platinum', 'Платинум'),
    ]
    PROJECT_COMPLETION_PERCENTAGE_CHOICES = [
        (0, 0),
        (25, 25),
        (50, 50),
        (75, 75),
        (100, 100),
    ]
    
    #TODO: сделать primary key
    user = models.OneToOneField(
        to = User,
        on_delete=models.CASCADE,
        related_name='client_user'
        )
    recommendation_status = models.CharField(
        max_length=10,
        choices=RECOMMENDATION_STATUS_CHOICES,
        default='silver',
        verbose_name="Статус рекомендации"
    )
    project_completion_percentage = models.PositiveIntegerField(
        default=0,
        choices=PROJECT_COMPLETION_PERCENTAGE_CHOICES,
        verbose_name="Процент завершенности проекта"
    )
    city = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Город")
    referral_code = models.OneToOneField(
        'ReferralCode',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_referral'
        )
    referral_code_used = models.PositiveIntegerField(
        default=0,
        verbose_name="Число использований реферального кода пользователя"
        )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиент"

    def __str__(self):
        return self.user.username
    

class ReferralCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)  
    active = models.BooleanField(default=True)
    uses_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.code