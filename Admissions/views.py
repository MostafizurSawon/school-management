import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from django.http import HttpResponse
from formtools.wizard.views import SessionWizardView

from .forms import (
    HscAdmissionScienceForm,
    ParentInfoForm,
    AddressForm,
    AcademicInformationForm,
    PaymentForm,
)
from .models import (
    HscScienceCompulsorySubjects,
    HscScienceOptionalSubjects,
    HscScienceMainSubjects,
    HscScienceFourthSubjects,
    HscFeeType,
)

# Form steps
FORMS = [
    ("admission", HscAdmissionScienceForm),
    ("parent",    ParentInfoForm),
    ("address",   AddressForm),
    ("academic",  AcademicInformationForm),
    ("payment",   PaymentForm),
]

# File storage for file uploads
file_storage = FileSystemStorage(
    location=os.path.join(settings.MEDIA_ROOT, "hsc-science", "tmp")
)

# Success view after form submission
def admission_success(request):
    return HttpResponse("<h2>Admission submitted successfully!</h2>")

# Main class for the form wizard (multi-step form)
class AdmissionWizard(SessionWizardView):
    form_list     = FORMS
    template_name = "admission_form_science.html"
    file_storage  = file_storage

    def post(self, request, *args, **kwargs):
        if "wizard_goto_step" in request.POST:
            return self.render_goto_step(request.POST["wizard_goto_step"])
        
        form = self.get_form(data=request.POST, files=request.FILES)
        print(f"POST data for step {self.steps.current}: {request.POST}")
        if not form.is_valid():
            print(f"Errors in step {self.steps.current}: {form.errors}")
        
        return super().post(request, *args, **kwargs)

    # Context data for each step (academic, payment)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.steps.current == 'academic':
            context['compulsory_subjects'] = HscScienceCompulsorySubjects.objects.filter(is_active=True)
            context['optional_subjects'] = HscScienceOptionalSubjects.objects.filter(is_active=True)
            context['main_subjects'] = HscScienceMainSubjects.objects.filter(is_active=True)
            context['fourth_subjects'] = HscScienceFourthSubjects.objects.filter(is_active=True)
        if self.steps.current == 'payment':
            context['fee_types'] = HscFeeType.objects.all()
        return context

    # Pass additional arguments to the forms (e.g., hsc_session in payment form)
    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        if step == 'payment':
            admission_form = self.get_form(step='admission')
            if admission_form.is_valid():
                hsc_session = admission_form.cleaned_data.get('hsc_session')
                kwargs.update({'hsc_session': hsc_session})
        return kwargs

    # Final action after the wizard is completed
    def done(self, form_list, **kwargs):
        admission = form_list[0].save()
        parent = form_list[1].save(commit=False)
        address = form_list[2].save(commit=False)
        academic = form_list[3].save(commit=False)
        payment = form_list[4].save(commit=False)

        academic.student = admission
        academic.save()

        academic.compulsorySubjects.set(HscScienceCompulsorySubjects.objects.filter(is_active=True))
        academic.optionalSubjects.set(HscScienceOptionalSubjects.objects.filter(is_active=True))
        academic.mainSubjects = form_list[3].cleaned_data.get('mainSubjects')
        academic.FourSubjects = form_list[3].cleaned_data.get('FourSubjects')
        academic.save()

        parent.student = admission
        address.student = admission
        payment.student = admission

        parent.save()
        address.save()
        payment.save()

        return redirect("admission_success")
