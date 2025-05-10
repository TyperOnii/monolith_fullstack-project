from django.contrib import admin

from core.apps.projects.models.projects import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'description','created_at', 'updated_at',)