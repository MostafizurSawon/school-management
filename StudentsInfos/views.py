from django.shortcuts import render, get_object_or_404, redirect
from Admissions.models import HscAdmissionScience, ParentInfo, Address, AcademicInformation, Payment
from Admissions.forms import ParentInfoForm, AddressForm, AcademicInformationForm, PaymentForm

def scienceStudents(request):
    students = HscAdmissionScience.objects.all().order_by('-id')  # latest first
    for student in students:
        print("demo ->", student)
    context = {
        'students': students,
    }
    return render(request, 'science-students.html', context)

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




