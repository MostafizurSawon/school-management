from django import forms
from .models import Exam, Group, Subject

class ExamForm(forms.ModelForm):
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Exam
        fields = ['exam_level', 'group', 'name', 'exam_date', 'subjects']
        widgets = {
            'exam_level': forms.Select(attrs={'id': 'id_exam_level'}),
            'group': forms.Select(attrs={'id': 'id_group'}),
            'exam_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialize group queryset empty by default
        self.fields['group'].queryset = Group.objects.none()

        if 'exam_level' in self.data:
            try:
                exam_level_id = int(self.data.get('exam_level'))
                self.fields['group'].queryset = Group.objects.filter(exam_level_id=exam_level_id).order_by('name')
            except (ValueError, TypeError):
                pass

        if 'group' in self.data:
            try:
                group_id = int(self.data.get('group'))
                self.fields['subjects'].queryset = Subject.objects.filter(group_id=group_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            # For editing existing exam
            self.fields['group'].queryset = Group.objects.filter(exam_level=self.instance.exam_level)
            self.fields['subjects'].queryset = self.instance.subjects.all()
