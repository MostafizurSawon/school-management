from django.urls import path
from . import views

urlpatterns = [
    path('science-info/', views.scienceStudents, name='science_students'),

    # Science Students
    path('edit-student/<int:pk>/', views.editStudent, name='edit_student'),
    path('delete-student/<int:pk>/', views.deleteStudent, name='delete_student'),

]


