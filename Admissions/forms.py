from django import forms
from .models import HscAdmissionScience, ParentInfo, Address, AcademicInformation, Payment

class HscAdmissionScienceForm(forms.ModelForm):
    birthdate = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        label="Date of Birth"
    )
    class Meta:
        model = HscAdmissionScience
        exclude = []

class ParentInfoForm(forms.ModelForm):
    fathers_date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    mothers_date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    guardian_date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
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
    payment_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    class Meta:
        model = Payment
        exclude = ['student']
