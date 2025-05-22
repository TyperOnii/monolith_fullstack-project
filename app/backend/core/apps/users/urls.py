from django.urls import path

from core.apps.users.views import users as users_views

urlpatterns = [
    path('users/registration/', users_views.RegistrationView.as_view(), name='registration'),
    path('users/change-password/', users_views.ChangePasswordView.as_view(), name='change-password'),
    path('users/me/', users_views.MeView.as_view(), name='me'),

]
