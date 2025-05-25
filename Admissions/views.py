# Admissions/views.py

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

# Step-by-step form definitions
FORMS = [
    ("admission", HscAdmissionScienceForm),
    ("parent",    ParentInfoForm),
    ("address",   AddressForm),
    ("academic",  AcademicInformationForm),
    ("payment",   PaymentForm),
]

# Temporary file storage for file uploads
file_storage = FileSystemStorage(
    location=os.path.join(settings.MEDIA_ROOT, "hsc-science", "tmp")
)

def admission_success(request):
    return HttpResponse("<h2>Admission submitted successfully!</h2>")

class AdmissionWizard(SessionWizardView):
    form_list     = FORMS
    template_name = "admission_form_science.html"
    file_storage  = file_storage

    def post(self, request, *args, **kwargs):
        # 1) if "Previous" was clicked, immediately render that step (skip validation)
        if "wizard_goto_step" in request.POST:
            return self.render_goto_step(request.POST["wizard_goto_step"])
        # 2) otherwise run normal validation / next-step logic
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # (you can still inspect context['wizard'] here if you like)
        return context

    def done(self, form_list, **kwargs):
        # save each step in order and link them together
        admission = form_list[0].save()
        parent    = form_list[1].save(commit=False)
        address   = form_list[2].save(commit=False)
        academic  = form_list[3].save(commit=False)
        payment   = form_list[4].save(commit=False)

        parent.student   = admission
        address.student  = admission
        academic.student = admission
        payment.student  = admission

        parent.save()
        address.save()
        academic.save()
        payment.save()

        return redirect("admission_success")



