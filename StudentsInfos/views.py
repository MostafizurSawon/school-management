from django.shortcuts import render, get_object_or_404, redirect
from Admissions.models import HscAdmissionScience, ParentInfo, Address, AcademicInformation, Payment
from Admissions.forms import ParentInfoForm, AddressForm, AcademicInformationForm, PaymentForm
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from django.http import HttpResponse
import os
from django.conf import settings

import pdfkit

# from weasyprint import HTML
# import tempfile

def scienceStudents(request):
    students = HscAdmissionScience.objects.all().order_by('-id')  # latest first
    # for student in students:
    #     print("demo ->", student)
    context = {
        'students': students,
    }
    return render(request, 'science-students.html', context)


def generate_student_pdf(request, pk):
    student = get_object_or_404(HscAdmissionScience, pk=pk)


    photo_path = os.path.join(settings.MEDIA_ROOT, student.photo.name)

    html = render_to_string("student_pdf_template.html", {
        "student": student,
        "photo_path": photo_path,
    })
    print("path ----->",photo_path)
    response = HttpResponse(content_type="application/pdf")
    pisa.CreatePDF(html, dest=response)
    return response



# def generate_student_pdf(request, pk):
#     student = get_object_or_404(HscAdmissionScience, pk=pk)

#     html_string = render_to_string("student_pdf_template.html", {"student": student})
    
#     # Create a temporary PDF file
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'filename=student_{student.pk}.pdf'

#     HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response)

#     return response

import pdfkit
from django.template.loader import render_to_string
from django.http import HttpResponse

def generate_student_pdf(request, pk):
    student = get_object_or_404(HscAdmissionScience, pk=pk)
    html = render_to_string("student_pdf_template.html", {"student": student})

    # Path to wkhtmltopdf binary (if not in PATH)
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

    pdf = pdfkit.from_string(html, False, configuration=config)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="student_{student.pk}.pdf"'
    return response




def editStudent(request, pk):
    admission = get_object_or_404(HscAdmissionScience, pk=pk)
    # load forms with instance for editing
    # optionally redirect to a custom edit form or use a wizard instance
    return render(request, 'edit-student.html', {'student': admission})

def deleteStudent(request, pk):
    student = get_object_or_404(HscAdmissionScience, pk=pk)
    
    if request.method == "POST":
        student.delete()
        return redirect('science_students')
    return render(request, 'confirm_delete.html', {'student': student})




