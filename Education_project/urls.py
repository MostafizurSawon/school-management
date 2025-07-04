"""
URL configuration for Education_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from . import views
from UserProfiles.views import notice_list

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.home, name='home'),
    path('', notice_list, name='home'),
    path('contact/', views.contact, name='contact'),
    path('accounts/', include('UserProfiles.urls')),
    path('admissions/', include('Admissions.urls')),
    path('student-infos/', include('StudentsInfos.urls')),
    path('exam/', include('Exams.urls', namespace='exams')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




# https://cms.pochamariacollege.edu.bd/form/science.php
# https://college.pochamariacollege.edu.bd/exams/create
# 