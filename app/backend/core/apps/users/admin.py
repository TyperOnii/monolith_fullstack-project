from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

from core.apps.users.models import Admin, Client

User = get_user_model()

class AdminInline(admin.StackedInline):
    model = Admin
    can_delete = False
    verbose_name = "Профиль администратора"
    readonly_fields = ('created_at', 'updated_at')

class ClientInline(admin.StackedInline):
    model = Client
    can_delete = False
    verbose_name = "Профиль клиента"
    readonly_fields = ('referral_code_used',)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    change_user_password_template = None
    list_display = ('username', 'email', 'role')
    list_display_links = ('username',)
    list_filter = ('role',)
    search_fields = ('username', 'email',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('email',)}),
        ('Права и роли', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
    )
    inlines = [AdminInline, ClientInline]

    def get_inline_instances(self, request, obj=None):
        """Показывает только нужный inline-профиль"""
        if not obj:
            return []
        if obj.role == 'admin':
            return [AdminInline(self.model, self.admin_site)]
        elif obj.role == 'client':
            return [ClientInline(self.model, self.admin_site)]
        return []

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        # Удаляем старый профиль при смене роли
        if change:
            old_user = User.objects.get(pk=obj.pk)
            if old_user.role != obj.role:
                self._delete_old_profile(old_user)

        self._create_profile(obj)

    def _delete_old_profile(self, user):
        """Удаляет профиль, не соответствующий текущей роли"""
        if user.role == 'admin' and hasattr(user, 'client_user'):
            user.client_user.delete()
        elif user.role == 'client' and hasattr(user, 'admin_user'):
            user.admin_user.delete()

    def _create_profile(self, user):
        """Создает профиль в зависимости от роли"""
        if user.role == 'admin' and not hasattr(user, 'admin_user'):
            Admin.objects.create(user=user)
        elif user.role == 'client' and not hasattr(user, 'client_user'):
            Client.objects.create(user=user)


