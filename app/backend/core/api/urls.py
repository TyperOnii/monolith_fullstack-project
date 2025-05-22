from core.api.spectacular.urls import urlpatterns as doc_urls
from django.urls import path, include

from core.apps.users.urls import urlpatterns as users_urls

app_name = 'api'
# сюда импортировать v1 router as v1_router и инклюдить к основному роутеру
urlpatterns = [
    path('auth/', include('djoser.urls.jwt')),
]

urlpatterns += doc_urls

urlpatterns += users_urls

# def custom_preprocessing_filter(endpoints):
#     filtered = []
#     for path, path_regex, method, callback in endpoints:
#         if '/auth/' in path:
#             callback.__dict__['tags'] = ['auth']
#         else:
#             callback.__dict__['tags'] = ['api']
#         filtered.append((path, path_regex, method, callback))
#     return filtered

# SPECTACULAR_SETTINGS['PREPROCESSING_HOOKS'] = [
#     'api.urls.custom_preprocessing_filter'
# ]