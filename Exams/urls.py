from django.urls import path
from .views import ExamCreateView, load_groups, load_subjects

app_name = 'exams'

urlpatterns = [
    path('add/', ExamCreateView.as_view(), name='create'),
    path('ajax/load-groups/', load_groups, name='ajax_load_groups'),
    path('ajax/load-subjects/', load_subjects, name='ajax_load_subjects'),
]
