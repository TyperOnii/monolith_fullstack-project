from rest_framework.filters import BaseFilterBackend


class MyProjectBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        return queryset.filter(created_by=user)