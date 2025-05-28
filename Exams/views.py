from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.http import JsonResponse
from .models import Group, Subject
from .forms import ExamForm
from .models import Exam
from django.contrib.auth.decorators import login_required

# @login_required
class ExamCreateView(CreateView):
    model = Exam
    form_class = ExamForm
    template_name = 'exams/exam_form.html'
    success_url = reverse_lazy('exams:create')

    def form_valid(self, form):
        # Save the exam instance first (without subjects)
        response = super().form_valid(form)

        # Get selected subjects from POST data
        subjects_ids = self.request.POST.getlist('subjects')
        if subjects_ids:
            self.object.subjects.set(subjects_ids)
        else:
            self.object.subjects.clear()

        return response

# AJAX views to fetch Groups and Subjects dynamically

def load_groups(request):
    exam_level_id = request.GET.get('exam_level')
    groups = Group.objects.filter(exam_level_id=exam_level_id).order_by('name')
    return JsonResponse(list(groups.values('id', 'name')), safe=False)

def load_subjects(request):
    group_id = request.GET.get('group')
    subjects = Subject.objects.filter(group_id=group_id).order_by('name')
    return JsonResponse(list(subjects.values('id', 'name')), safe=False)




class ExamListView(ListView):
    model = Exam
    template_name = 'exams/exam_list.html'
    context_object_name = 'exams'

class ExamDetailView(DetailView):
    model = Exam
    template_name = 'exams/exam_detail.html'

class ExamUpdateView(UpdateView):
    model = Exam
    form_class = ExamForm
    template_name = 'exams/exam_form.html'
    success_url = reverse_lazy('exams:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        subjects_ids = self.request.POST.getlist('subjects')
        if subjects_ids:
            self.object.subjects.set(subjects_ids)
        else:
            self.object.subjects.clear()
        return response

class ExamDeleteView(DeleteView):
    model = Exam
    template_name = 'exams/exam_confirm_delete.html'
    success_url = reverse_lazy('exams:list')
