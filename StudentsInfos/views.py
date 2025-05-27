from django.shortcuts import render, get_object_or_404, redirect
from Admissions.models import HscAdmissionScience, ParentInfo, Address, AcademicInformation, Payment, HscSession
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from django.http import HttpResponse
import os
from django.conf import settings
from Admissions.forms import (
    HscAdmissionScienceForm, ParentInfoForm, AddressForm,
    AcademicInformationForm, PaymentForm
)

# import pdfkit





# from weasyprint import HTML


# from weasyprint import HTML
# import tempfile

def scienceStudents(request):
    # 1. grab all sessions
    sessions = HscSession.objects.all().order_by('-session')

    # 2. check for a session filter in the querystring
    session_id = request.GET.get('session')
    if session_id:
        # if provided, only students in that session
        students = HscAdmissionScience.objects.filter(
            hsc_session_id=session_id
        ).select_related(
            'hsc_session', 'parent_info', 'address', 'academic_info', 'payment'
        ).order_by('-id')
        selected_session = get_object_or_404(HscSession, id=session_id)
    else:
        # otherwise show all
        students = HscAdmissionScience.objects.all().select_related(
            'hsc_session', 'parent_info', 'address', 'academic_info', 'payment'
        ).order_by('-id')
        selected_session = None

    return render(request, 'science-students.html', {
        'sessions': sessions,
        'students': students,
        'selected_session': selected_session,
    })






def editStudent(request, pk):
    admission = get_object_or_404(HscAdmissionScience, pk=pk)
    parent = get_object_or_404(ParentInfo, student=admission)
    address = get_object_or_404(Address, student=admission)
    academic = get_object_or_404(AcademicInformation, student=admission)
    payment = get_object_or_404(Payment, student=admission)

    if request.method == 'POST':
        admission_form = HscAdmissionScienceForm(request.POST, request.FILES, instance=admission)
        parent_form = ParentInfoForm(request.POST, instance=parent)
        address_form = AddressForm(request.POST, instance=address)
        academic_form = AcademicInformationForm(request.POST, instance=academic)
        payment_form = PaymentForm(request.POST, instance=payment)

        if all([admission_form.is_valid(), parent_form.is_valid(), address_form.is_valid(), academic_form.is_valid(), payment_form.is_valid()]):
            admission_form.save()
            parent_form.save()
            address_form.save()
            academic_form.save()
            payment_form.save()
            return redirect('science_students')
    else:
        admission_form = HscAdmissionScienceForm(instance=admission)
        parent_form = ParentInfoForm(instance=parent)
        address_form = AddressForm(instance=address)
        academic_form = AcademicInformationForm(instance=academic)
        payment_form = PaymentForm(instance=payment)

    context = {
        'admission_form': admission_form,
        'parent_form': parent_form,
        'address_form': address_form,
        'academic_form': academic_form,
        'payment_form': payment_form,
    }
    return render(request, 'edit-student.html', context)



def deleteStudent(request, pk):
    student = get_object_or_404(HscAdmissionScience, pk=pk)
    
    if request.method == "POST":
        student.delete()
        return redirect('science_students')
    return render(request, 'confirm_delete.html', {'student': student})


# def generate_student_pdf(request, pk):
#     student = get_object_or_404(HscAdmissionScience, pk=pk)
#     html = render_to_string("student_pdf_template.html", {"student": student})
#     response = HttpResponse(content_type="application/pdf")
#     pisa.CreatePDF(html, dest=response)
#     return response

def generate_student_pdf(request, pk):
    student = get_object_or_404(HscAdmissionScience, pk=pk)
    parent = getattr(student, 'parentinfo', None)
    address = getattr(student, 'address', None)
    academic = getattr(student, 'academicinformation', None)
    payment = getattr(student, 'payment', None)

    context = {
        'student': student,
        'parent': parent,
        'address': address,
        'academic': academic,
        'payment': payment,
    }

    return render(request, 'student_pdf_template.html', context)

