from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.apps.projects import views

router = DefaultRouter()
router.register(r'', views.ProjectListViewSet, basename='projects')

urlpatterns = [
    path('projects/', include(router.urls)),
]
