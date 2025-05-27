from django import forms
from .models import (
    HscAdmissionScience, ParentInfo, Address, AcademicInformation, Payment,
    HscScienceCompulsorySubjects, HscScienceMainSubjects,
    HscScienceFourthSubjects, HscFeeType, HscScienceOptionalSubjects
)

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
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    mothers_date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    guardian_date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )

    class Meta:
        model = ParentInfo
        exclude = ['student']
        widgets = {
            'guardian': forms.Select(attrs={'id': 'id_guardian'}),
        }

    def clean(self):
        cleaned = super().clean()
        guardian = cleaned.get('guardian')

        if guardian == 'Other':
            for name in (
                'guardian_name_english',
                'guardian_date_of_birth',  # Optional but required if guardian == Other
                'guardian_nid',
                'guardian_mobile',
            ):
                if not cleaned.get(name):
                    self.add_error(
                        name,
                        "This field is required when guardian is “Other.”"
                    )
        return cleaned

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['student']
        widgets = {
            'permanent_address_same': forms.CheckboxInput(attrs={'id': 'id_copy_address'}),
        }







class AcademicInformationForm(forms.ModelForm):
    compulsorySubjects = forms.ModelMultipleChoiceField(
        queryset=HscScienceCompulsorySubjects.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple(attrs={'disabled': 'disabled'}),
        required=False,
    )
    optionalSubjects = forms.ModelMultipleChoiceField(
        queryset=HscScienceOptionalSubjects.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple(attrs={'disabled': 'disabled'}),
        required=False,
    )
    mainSubjects = forms.ModelChoiceField(
        queryset=HscScienceMainSubjects.objects.filter(is_active=True),
        widget=forms.RadioSelect(),
        required=False,
    )
    FourSubjects = forms.ModelChoiceField(
        queryset=HscScienceFourthSubjects.objects.filter(is_active=True),
        widget=forms.RadioSelect(),
        required=False,
    )

    class Meta:
        model = AcademicInformation
        exclude = ['student']
        widgets = {
            'ssc_session': forms.Select(attrs={'class': 'form-select'}),
            'ssc_board': forms.Select(attrs={'class': 'form-select'}),
            'ssc_year': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        main_subjects = cleaned_data.get('mainSubjects')
        fourth_subjects = cleaned_data.get('FourSubjects')
        if main_subjects and fourth_subjects and main_subjects == fourth_subjects:
            self.add_error('FourSubjects', 'The 4th subject cannot be the same as the main subject.')
        return cleaned_data


class PaymentForm(forms.ModelForm):
    payment_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Payment
        exclude = ['student']
        widgets = {
            'amount': forms.NumberInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        hsc_session = kwargs.pop('hsc_session', None)
        super().__init__(*args, **kwargs)

        if hsc_session and hsc_session.fee:
            self.fields['amount'].initial = hsc_session.fee.amount
        else:
            try:
                admission_fee = HscFeeType.objects.get(fee_type__iexact='Admission')
                self.fields['amount'].initial = admission_fee.amount
            except HscFeeType.DoesNotExist:
                self.fields['amount'].initial = 0
