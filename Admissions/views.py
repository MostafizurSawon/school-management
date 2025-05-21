from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from formtools.wizard.views import SessionWizardView
from .forms import (
    HscAdmissionScienceForm, ParentInfoForm, AddressForm,
    AcademicInformationForm, PaymentForm
)
import os
from django.http import HttpResponse



FORMS = [
    ("admission", HscAdmissionScienceForm),
    ("parent", ParentInfoForm),
    ("address", AddressForm),
    ("academic", AcademicInformationForm),
    ("payment", PaymentForm),
]

def admission_success(request):
    return HttpResponse("<h2>Admission submitted successfully!</h2>")

file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'hsc-science', 'tmp'))

class AdmissionWizard(SessionWizardView):
    form_list = FORMS
    file_storage = file_storage
    template_name = "admission_form_science.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("Wizard context:", context['wizard'])  # Debug
        return context

    def done(self, form_list, **kwargs):
        admission = form_list[0].save()
        parent = form_list[1].save(commit=False)
        address = form_list[2].save(commit=False)
        academic = form_list[3].save(commit=False)
        payment = form_list[4].save(commit=False)

        parent.student = admission
        address.student = admission
        academic.student = admission
        payment.student = admission

        parent.save()
        address.save()
        academic.save()
        payment.save()

        return redirect('admission_success')





