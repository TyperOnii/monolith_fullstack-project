from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(('core.api.urls', 'api'), namespace='api')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
]

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls
    urlpatterns += debug_toolbar_urls()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  


def custom_preprocessing_filter(endpoints):
    filtered = []
    for path, path_regex, method, callback in endpoints:
        # Для эндпоинтов /api/auth/
        if path.startswith('/api/auth/'):
            callback.__dict__['tags'] = ['auth']
        # Для остальных эндпоинтов /api/
        elif path.startswith('/api/'):
            callback.__dict__['tags'] = ['api']
        filtered.append((path, path_regex, method, callback))
    return filtered