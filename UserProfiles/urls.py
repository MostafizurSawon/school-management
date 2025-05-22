from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/general-settings/', views.site_settings_view, name='general_settings'),
    path('profile/portal-notice/', views.create_notice, name='portal-notice'),
]