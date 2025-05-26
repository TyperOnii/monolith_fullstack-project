from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.apps.projects import views

router = DefaultRouter()
router.register(r'', views.ProjectSearchListView, basename='projects')
router.register(r'manage', views.ProjectView, basename='projects-manage')

urlpatterns = [
    path('projects/', include(router.urls)),
]
