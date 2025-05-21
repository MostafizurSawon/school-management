from django import forms
from .models import HscAdmissionScience, ParentInfo, Address, AcademicInformation, Payment

class HscAdmissionScienceForm(forms.ModelForm):
    class Meta:
        model = HscAdmissionScience
        exclude = []

class ParentInfoForm(forms.ModelForm):
    class Meta:
        model = ParentInfo
        exclude = ['student']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['student']

class AcademicInformationForm(forms.ModelForm):
    class Meta:
        model = AcademicInformation
        exclude = ['student']

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ['student']
