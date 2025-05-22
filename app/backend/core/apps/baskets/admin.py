from django.contrib import admin

from core.apps.baskets.models import Basket


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('user', 'project_service', 'session_key', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user', 'project_service', 'session_key')
    readonly_fields = ('created_at', 'updated_at')
    