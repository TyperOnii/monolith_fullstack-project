from django.contrib import admin

from core.apps.projects.models import Project, ProjectSpecifications, Service, ProjectService, ProjectImage, ProjectCategory
from django.db.models import Count

class ProjectSpecificationsInline(admin.StackedInline):
    model = ProjectSpecifications
    verbose_name = "Характеристики проекта"
    verbose_name_plural = "Характеристики проекта"
    can_delete = False  
    extra = 1  

class ProjectImageInline(admin.StackedInline):
    model = ProjectImage
    verbose_name = "Изображение проекта"
    verbose_name_plural = "Изображения проекта"
    can_delete = True  
    extra = 1

class ProjectServiceInline(admin.TabularInline):
    model = ProjectService  
    extra = 1  
    verbose_name = "Услуга в проекте"
    verbose_name_plural = "Услуги в проекте"
    fields = ("service", "price", "download_link") 
    autocomplete_fields = ["service"] 

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Фильтрация услуг (опционально)
        if db_field.name == "service":
            kwargs["queryset"] = Service.objects.all().order_by("title")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'description','created_at', 'updated_at', 'count_services',)
    list_display_links = ('id', 'title',)
    readonly_fields = ('count_services',)
    search_fields = ("title", "description")
    list_filter = ('created_at', 'updated_at', 'is_visible')
    ordering = ('title',)
    inlines = [ProjectSpecificationsInline, ProjectServiceInline, ProjectImageInline] 

    def count_services(self, obj):
        return obj.count_services
    count_services.short_description = 'Количество услуг'

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(count_services=Count('services'))


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description',)
    list_display_links = ('id', 'title',)
    search_fields = ("title", "description") 
    ordering = ('title',)



@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug" :("floor","the_area_filter","price_filter")}
    fields = ("floor","the_area_filter","price_filter","slug")
    list_display = ('id', 'floor', 'the_area_filter', 'price_filter', 'slug')
    list_display_links = ('id', 'floor',)
    search_fields = ("floor", "the_area_filter", "price_filter", "slug")
    ordering = ('floor', 'the_area_filter', 'price_filter')
    




# @admin.register(ProjectSpecifications)
# class ProjectSpecificationsAdmin(admin.ModelAdmin):
