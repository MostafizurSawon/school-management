from django.contrib import admin
from .models import ExamLevel, Group, Subject, Exam

@admin.register(ExamLevel)
class ExamLevelAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'exam_level')
    list_filter = ('exam_level',)
    search_fields = ('name',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'exam_level', 'group')
    list_filter = ('exam_level', 'group')
    search_fields = ('name',)

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'exam_level', 'group', 'exam_date')
    list_filter = ('exam_level', 'group')
    filter_horizontal = ('subjects',)
