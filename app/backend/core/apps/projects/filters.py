import django_filters
from django.db.models import Q, F
from django_filters.rest_framework import filters

from core.apps.projects.models import Project, ProjectService


class ProjectFilter(django_filters.FilterSet):
    is_visible = django_filters.BooleanFilter('is_visible', label='Виден ли проект в каталоге')
    #can_manage = django_filters.BooleanFilter('can_manage', label='Можно ли менять проект')

    class Meta:
        model = Project
        fields = ('is_visible', 'id',)


class ProjectServiceFilter(django_filters.FilterSet):
    project = filters.NumberFilter(field_name='project', lookup_expr='exact')
    service = filters.NumberFilter(field_name='service', lookup_expr='exact')
    price = filters.RangeFilter(field_name='price', lookup_expr='range')

    class Meta:
        model = ProjectService
        fields = ('project', 'service', 'price',)