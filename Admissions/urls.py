# urls.py
from django.urls import path
from .views import AdmissionWizard
from .views import admission_success

urlpatterns = [
    path('hsc-science-admission/', AdmissionWizard.as_view(), name='hsc_science_admission'),
    path('hsc-science-admission/success/', admission_success, name='admission_success'),
]
