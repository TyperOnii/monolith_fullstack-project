import django_filters
from django.db.models import Q, F

from core.apps.projects.models.projects import Project


class ProjectFilter(django_filters.FilterSet):
    is_visible = django_filters.BooleanFilter('is_visible', label='Виден ли проект в каталоге')
    #can_manage = django_filters.BooleanFilter('can_manage', label='Можно ли менять проект')

    class Meta:
        model = Project
        fields = ('is_visible', 'id',)