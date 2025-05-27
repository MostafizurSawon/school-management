from django.urls import path
from .views import (
    AdmissionScienceWizard, AdmissionArtsWizard, AdmissionCommerceWizard,
    admission_success, add_admission_fee
)

urlpatterns = [
    # Science Admission
    path('hsc-science-admission/', AdmissionScienceWizard.as_view(), name='hsc_science_admission'),

    # Arts Admission
    path('hsc-arts-admission/', AdmissionArtsWizard.as_view(), name='hsc_arts_admission'),

    # Commerce Admission
    path('hsc-commerce-admission/', AdmissionCommerceWizard.as_view(), name='hsc_commerce_admission'),

    # Common Success Page
    path('admission-success/', admission_success, name='admission_success'),
    path('add-admission-fee/', add_admission_fee, name='add_admission_fee'),
]
