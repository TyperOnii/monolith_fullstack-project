from core.apps.users.urls import urlpatterns as users_urls
from core.apps.projects.urls import urlpatterns as projects_urls
from core.apps.baskets.urls import urlpatterns as baskets_urls



urlpatterns = []

urlpatterns += users_urls
urlpatterns += projects_urls
urlpatterns += baskets_urls