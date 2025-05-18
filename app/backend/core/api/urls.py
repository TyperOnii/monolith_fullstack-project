from core.api.spectacular.urls import urlpatterns as doc_urls
from django.urls import path, include
app_name = 'api'
# сюда импортировать v1 router as v1_router и инклюдить к основному роутеру
urlpatterns = [
    path('auth/', include('djoser.url.jwt'))
]

urlpatterns += doc_urls