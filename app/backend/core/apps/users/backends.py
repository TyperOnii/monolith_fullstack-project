from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserBackend:
    supports_object_permissions = True
    supports_anonymous_user = True
    supports_inactive_user = True

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(
                Q(username=username) | 
                Q(email=username) | 
                Q(phone_number=username)
            )
            #print(f"user: {username}")
        except User.DoesNotExist:
            return None
        if not user.check_password(password):
            return None
        print(f"Успешная аутентификация {username}")
        return user