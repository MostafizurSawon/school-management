from django.urls import path
from .views import ExamCreateView, load_groups, load_subjects, ExamListView, ExamDetailView, ExamUpdateView, ExamDeleteView

app_name = 'exams'

urlpatterns = [
    path('add/', ExamCreateView.as_view(), name='create'),
    path('', ExamListView.as_view(), name='list'),
    path('<int:pk>/', ExamDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', ExamUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', ExamDeleteView.as_view(), name='delete'),
    path('ajax/load-groups/', load_groups, name='ajax_load_groups'),
    path('ajax/load-subjects/', load_subjects, name='ajax_load_subjects'),
]
