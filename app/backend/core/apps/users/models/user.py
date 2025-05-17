from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


class User(AbstractUser):
    ROLE_CHOISES = [
        ('client',"Обычный пользователь"),
        ('admin','Администратор сайта'),
    ]

    role = models.CharField(choices=ROLE_CHOISES, max_length=128, default='client', verbose_name="Роль пользователя")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Номер телефона пользователя")
    is_verified_email = models.BooleanField(default=False, blank=True, verbose_name="Подтвержден ли email")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
    
    def __str__(self):
        return self.username
    

class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self) -> str:
        return f"EmailVerification object for {self.user}"

    def send_verification_email(self):
        link = reverse("users:email_ver", kwargs={"email": self.user.email, "code": self.code})
        verification_link = f"{settings.DOMAIN_NAME}{link}"
        subject = f"Подтверждение учетной записи для {self.user.username}"
        message = f"Для подтверждения учетной записи для {self.user.email} перейдите по ссылке {verification_link}"
        

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return True if now() >= self.expiration else False