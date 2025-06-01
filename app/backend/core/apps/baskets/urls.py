from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.apps.baskets.views.basket import BasketViewSet

router = DefaultRouter()
router.register(r'', BasketViewSet, basename='basket')

urlpatterns = [
    path('baskets/', include(router.urls)),
]