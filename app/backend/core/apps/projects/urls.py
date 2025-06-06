from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.apps.projects import views

router = DefaultRouter()
router.register(r'', views.ProjectSearchListView, basename='projects')
router.register(r'manage', views.ProjectView, basename='projects-manage')
router.register(r'images', views.ProjectImagesView, basename='projects-images')
router.register(r'services', views.ServiceView, basename='projects-services')
router.register(r'project-services', views.ProjectServiceView, basename='projects-project-services')

urlpatterns = [
    path('projects/', include(router.urls)),
]
