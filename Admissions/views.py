import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from formtools.wizard.views import SessionWizardView
from django.shortcuts import render, redirect
from django.contrib import messages


from .forms import (
    # Science
    HscAdmissionScienceForm, ParentInfoForm, AddressForm, AcademicInformationForm, PaymentForm,
    # Arts
    HscAdmissionArtsForm, ParentInfoArtsForm, AddressArtsForm, AcademicInformationArtsForm, PaymentArtsForm,
    # Commerce
    HscAdmissionCommerceForm, ParentInfoCommerceForm, AddressCommerceForm, AcademicInformationCommerceForm, PaymentCommerceForm, FeeStructureForm
)

from .models import (
    # Science
    HscScienceCompulsorySubjects, HscScienceOptionalSubjects, HscScienceMainSubjects, HscScienceFourthSubjects,
    # Arts
    HscArtsCompulsorySubjects, HscArtsOptionalSubjects, HscArtsMainSubjects, HscArtsFourthSubjects,
    # Commerce
    HscCommerceCompulsorySubjects, HscCommerceOptionalSubjects, HscCommerceMainSubjects, HscCommerceFourthSubjects,
    # Common
    HscFeeType, HscSession, HscSessionForPayment, ProgramType, Program, FeePurpose, FeeStructure
)

# === Shared Success View ===
def admission_success(request):
    return HttpResponse("<h2>Admission submitted successfully!</h2>")

# === File Storage ===
science_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "hsc-science", "tmp"))
arts_storage    = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "hsc-arts", "tmp"))
commerce_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "hsc-commerce", "tmp"))

# === Science Wizard ===
class AdmissionScienceWizard(SessionWizardView):
    form_list = [
        ("admission", HscAdmissionScienceForm),
        ("parent",    ParentInfoForm),
        ("address",   AddressForm),
        ("academic",  AcademicInformationForm),
        ("payment",   PaymentForm),
    ]
    template_name = "admission_form_science.html"
    file_storage  = science_storage

    def post(self, request, *args, **kwargs):
        if "wizard_goto_step" in request.POST:
            return self.render_goto_step(request.POST["wizard_goto_step"])
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.steps.current == 'academic':
            context.update({
                'compulsory_subjects': HscScienceCompulsorySubjects.objects.filter(is_active=True),
                'optional_subjects': HscScienceOptionalSubjects.objects.filter(is_active=True),
                'main_subjects': HscScienceMainSubjects.objects.filter(is_active=True),
                'fourth_subjects': HscScienceFourthSubjects.objects.filter(is_active=True),
            })
        if self.steps.current == 'payment':
            context['fee_types'] = HscFeeType.objects.all()
        return context

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        if step == 'payment':
            admission_form = self.get_form(step='admission')
            if admission_form.is_valid():
                kwargs.update({'hsc_session': admission_form.cleaned_data.get('hsc_session')})
        return kwargs

    def done(self, form_list, **kwargs):
        # Save Admission FIRST
        admission = form_list[0].save()

        # Now link and save related models
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

        # Save academic with subjects after linking
        academic.save()
        academic.compulsorySubjects.set(HscScienceCompulsorySubjects.objects.filter(is_active=True))  # For Science; adjust for Arts/Commerce
        academic.optionalSubjects.set(HscScienceOptionalSubjects.objects.filter(is_active=True))
        academic.mainSubjects = form_list[3].cleaned_data.get('mainSubjects')
        academic.FourSubjects = form_list[3].cleaned_data.get('FourSubjects')
        academic.save()

        payment.save()

        return redirect("admission_success")


# === Arts Wizard ===
class AdmissionArtsWizard(SessionWizardView):
    form_list = [
        ("admission", HscAdmissionArtsForm),
        ("parent",    ParentInfoArtsForm),
        ("address",   AddressArtsForm),
        ("academic",  AcademicInformationArtsForm),
        ("payment",   PaymentArtsForm),
    ]
    template_name = "admission_form_arts.html"
    file_storage  = arts_storage

    def post(self, request, *args, **kwargs):
        if "wizard_goto_step" in request.POST:
            return self.render_goto_step(request.POST["wizard_goto_step"])
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.steps.current == 'academic':
            context.update({
                'compulsory_subjects': HscArtsCompulsorySubjects.objects.filter(is_active=True),
                'optional_subjects': HscArtsOptionalSubjects.objects.filter(is_active=True),
                'main_subjects': HscArtsMainSubjects.objects.filter(is_active=True),
                'fourth_subjects': HscArtsFourthSubjects.objects.filter(is_active=True),
            })
        if self.steps.current == 'payment':
            context['fee_types'] = HscFeeType.objects.all()
        return context

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        if step == 'payment':
            admission_form = self.get_form(step='admission')
            if admission_form.is_valid():
                kwargs.update({'hsc_session': admission_form.cleaned_data.get('hsc_session')})
        return kwargs

    def done(self, form_list, **kwargs):
        admission, parent, address, academic, payment = [form.save(commit=False) for form in form_list]
        academic.student = admission
        academic.save()
        academic.compulsorySubjects.set(HscArtsCompulsorySubjects.objects.filter(is_active=True))
        academic.optionalSubjects.set(HscArtsOptionalSubjects.objects.filter(is_active=True))
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

# === Commerce Wizard ===
class AdmissionCommerceWizard(SessionWizardView):
    form_list = [
        ("admission", HscAdmissionCommerceForm),
        ("parent",    ParentInfoCommerceForm),
        ("address",   AddressCommerceForm),
        ("academic",  AcademicInformationCommerceForm),
        ("payment",   PaymentCommerceForm),
    ]
    template_name = "admission_form_commerce.html"
    file_storage  = commerce_storage

    def post(self, request, *args, **kwargs):
        if "wizard_goto_step" in request.POST:
            return self.render_goto_step(request.POST["wizard_goto_step"])
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.steps.current == 'academic':
            context.update({
                'compulsory_subjects': HscCommerceCompulsorySubjects.objects.filter(is_active=True),
                'optional_subjects': HscCommerceOptionalSubjects.objects.filter(is_active=True),
                'main_subjects': HscCommerceMainSubjects.objects.filter(is_active=True),
                'fourth_subjects': HscCommerceFourthSubjects.objects.filter(is_active=True),
            })
        if self.steps.current == 'payment':
            context['fee_types'] = HscFeeType.objects.all()
        return context

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        if step == 'payment':
            admission_form = self.get_form(step='admission')
            if admission_form.is_valid():
                kwargs.update({'hsc_session': admission_form.cleaned_data.get('hsc_session')})
        return kwargs

    def done(self, form_list, **kwargs):
        admission, parent, address, academic, payment = [form.save(commit=False) for form in form_list]
        academic.student = admission
        academic.save()
        academic.compulsorySubjects.set(HscCommerceCompulsorySubjects.objects.filter(is_active=True))
        academic.optionalSubjects.set(HscCommerceOptionalSubjects.objects.filter(is_active=True))
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








def add_admission_fee(request):
    if request.method == 'POST':
        form = FeeStructureForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Admission Fee added successfully.")
            return redirect('add_admission_fee')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = FeeStructureForm()

    fee_structures = FeeStructure.objects.select_related(
        'hsc_session', 'program_type', 'program', 'fee_purpose'
    ).all()

    return render(request, 'add_admission_fee.html', {
        'form': form,
        'fee_structures': fee_structures,
    })
