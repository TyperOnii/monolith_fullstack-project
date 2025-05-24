from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from phonenumber_field.modelfields import PhoneNumberField

from core.apps.users.managers import CustomUserManager



class User(AbstractUser):
    ROLE_CHOICES = [
        ('client',"Обычный пользователь"),
        ('admin','Администратор сайта'),
    ]

    # username = models.CharField(
    #     max_length=64,
    #     blank=True,
    #     null=True,
    #     unique=True,
    #     verbose_name="Логин пользователя"
    # )
    role = models.CharField(
        choices=ROLE_CHOICES,
        max_length=128,
        default='client',
        verbose_name="Роль пользователя"
        )
    phone_number = PhoneNumberField(
        null=True,
        blank=True,
        unique=True,
        verbose_name="Номер телефона пользователя"
        )
    is_verified_phone = models.BooleanField(
        default=False,
        blank=True,
        verbose_name="Подтвержден ли номер телефона"
    )
    email = models.EmailField(
        unique=True,
        blank=True,
        null=True,
        verbose_name="Email пользователя"
    )
    is_verified_email = models.BooleanField(
        default=False,
        blank=True,
        verbose_name="Подтвержден ли email"
        )
    
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="custom_user_set",  # Уникальное имя
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_set",  # Уникальное имя
        related_query_name="user",
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = "users_user"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        constraints = [
            models.UniqueConstraint(
                fields=['phone_number'],
                name='unique_phone_number',
                condition=models.Q(phone_number__isnull=False)
            ),
            models.UniqueConstraint(
                fields=['email'],
                name='unique_email',
                condition=models.Q(email__isnull=False)
            )
        ]

    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return f"{self.id} {self.username}"
    

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
    


# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if not hasattr(instance, ' admin_user') or not hasattr(instance, 'client_user') or created:
#         if instance.role == 'admin':
#             Admin.objects.create(user=instance)
#         elif instance.role == 'client':
#             Client.objects.create(user=instance)