from django import forms
from .models import (
    HscAdmissionScience, HscAdmissionArts, HscAdmissionCommerce,
    ParentInfo, ParentInfoArts, ParentInfoCommerce,
    Address, AddressArts, AddressCommerce,
    AcademicInformation, AcademicInformationArts, AcademicInformationCommerce,
    Payment, PaymentArts, PaymentCommerce,
    HscScienceCompulsorySubjects, HscScienceOptionalSubjects, HscScienceMainSubjects, HscScienceFourthSubjects,
    HscArtsCompulsorySubjects, HscArtsOptionalSubjects, HscArtsMainSubjects, HscArtsFourthSubjects,
    HscCommerceCompulsorySubjects, HscCommerceOptionalSubjects, HscCommerceMainSubjects, HscCommerceFourthSubjects,
    HscFeeType, HscSession, HscSessionForPayment, ProgramType, Program, FeePurpose, FeeStructure
)



from django.core.exceptions import ValidationError







# from .models import HscSessionForPayment, ProgramType, Program, FeePurpose, FeeStructure

class HscSessionForPaymentForm(forms.ModelForm):
    class Meta:
        model = HscSessionForPayment
        fields = ['session']
        widgets = {
            'session': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Session (e.g., 2024-2025)'}),
        }

class ProgramTypeForm(forms.ModelForm):
    class Meta:
        model = ProgramType
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Program Type (e.g., HSC, Degree)'}),
        }

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['program_type', 'name']
        widgets = {
            'program_type': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Program Name (e.g., Science, Arts)'}),
        }

class FeePurposeForm(forms.ModelForm):
    class Meta:
        model = FeePurpose
        fields = ['purpose_name']
        widgets = {
            'purpose_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Fee Purpose (e.g., Admission Fee, Exam Fee)'}),
        }







class FeeStructureForm(forms.ModelForm):
    class Meta:
        model = FeeStructure
        fields = ['hsc_session', 'program_type', 'program', 'fee_purpose', 'amount']
        widgets = {
            'hsc_session': forms.Select(attrs={'class': 'form-select'}),
            'program_type': forms.Select(attrs={'class': 'form-select'}),
            'program': forms.Select(attrs={'class': 'form-select'}),
            'fee_purpose': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Amount'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        program_type = cleaned_data.get('program_type')
        program = cleaned_data.get('program')

        if program and program_type and program.program_type != program_type:
            raise ValidationError("Selected program does not belong to the selected program type.")
    













# class HscSessionForm(forms.ModelForm):
#     class Meta:
#         model = HscSession
#         fields = ['session', 'fee']
#         widgets = {
#             'session': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Session (e.g., 2024-2025)'}),
#             'program_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Program Type (e.g., Science)'}),
#             'program': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Program (e.g., HSC)'}),
#             'fee': forms.Select(attrs={'class': 'form-select'}),
#         }


# ------------- Science Forms -------------
class HscAdmissionScienceForm(forms.ModelForm):
    birthdate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True, label="Date of Birth")
    class Meta:
        model = HscAdmissionScience
        exclude = ['type', 'program']

class ParentInfoForm(forms.ModelForm):
    fathers_date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    mothers_date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    guardian_date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = ParentInfo
        exclude = ['student']
        widgets = {'guardian': forms.Select(attrs={'id': 'id_guardian'})}

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('guardian') == 'Other':
            for name in ('guardian_name_english', 'guardian_date_of_birth', 'guardian_nid', 'guardian_mobile'):
                if not cleaned.get(name):
                    self.add_error(name, "This field is required when guardian is 'Other'.")
        return cleaned

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['student']
        widgets = {'permanent_address_same': forms.CheckboxInput(attrs={'id': 'id_copy_address'})}

class AcademicInformationForm(forms.ModelForm):
    compulsorySubjects = forms.ModelMultipleChoiceField(queryset=HscScienceCompulsorySubjects.objects.filter(is_active=True), widget=forms.CheckboxSelectMultiple(attrs={'disabled': 'disabled'}), required=False)
    optionalSubjects = forms.ModelMultipleChoiceField(queryset=HscScienceOptionalSubjects.objects.filter(is_active=True), widget=forms.CheckboxSelectMultiple(attrs={'disabled': 'disabled'}), required=False)
    mainSubjects = forms.ModelChoiceField(queryset=HscScienceMainSubjects.objects.filter(is_active=True), widget=forms.RadioSelect(), required=False)
    FourSubjects = forms.ModelChoiceField(queryset=HscScienceFourthSubjects.objects.filter(is_active=True), widget=forms.RadioSelect(), required=False)

    class Meta:
        model = AcademicInformation
        exclude = ['student']
        widgets = {'ssc_session': forms.Select(attrs={'class': 'form-select'}), 'ssc_board': forms.Select(attrs={'class': 'form-select'}), 'ssc_year': forms.Select(attrs={'class': 'form-select'})}

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('mainSubjects') == cleaned_data.get('FourSubjects'):
            self.add_error('FourSubjects', 'The 4th subject cannot be the same as the main subject.')
        return cleaned_data

# class PaymentForm(forms.ModelForm):
#     payment_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
#     class Meta:
#         model = Payment
#         exclude = ['student']
#         widgets = {'amount': forms.NumberInput(attrs={'readonly': 'readonly'})}

#     def __init__(self, *args, **kwargs):
#         hsc_session = kwargs.pop('hsc_session', None)
#         super().__init__(*args, **kwargs)
#         self.fields['amount'].initial = hsc_session.fee.amount if hsc_session and hsc_session.fee else HscFeeType.objects.filter(fee_type__iexact='Admission').first().amount if HscFeeType.objects.filter(fee_type__iexact='Admission').exists() else 0



class PaymentForm(forms.ModelForm):
    payment_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Payment
        exclude = ['student']
        widgets = {
            'amount': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'method': forms.Select(attrs={'class': 'form-select'}),
            'transaction_id': forms.TextInput(attrs={'class': 'form-control'}),
            'payment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'receipt_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        hsc_session = kwargs.pop('hsc_session', None)
        program_type = kwargs.pop('program_type', None)
        program = kwargs.pop('program', None)
        super().__init__(*args, **kwargs)

        admission_purpose = FeePurpose.objects.filter(purpose_name__iexact="Admission").first()

        fee_amount = None
        if hsc_session and program_type and program and admission_purpose:
            fee_entry = FeeStructure.objects.filter(
                hsc_session=hsc_session,
                program_type=program_type,
                program=program,
                fee_purpose=admission_purpose
            ).first()
            if fee_entry:
                fee_amount = fee_entry.amount

        self.fields['amount'].initial = fee_amount if fee_amount is not None else 0



# ------------- Arts Forms -------------
class HscAdmissionArtsForm(forms.ModelForm):
    birthdate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True, label="Date of Birth")
    class Meta:
        model = HscAdmissionArts
        exclude = ['type', 'program']

class ParentInfoArtsForm(forms.ModelForm):
    fathers_date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    mothers_date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    guardian_date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = ParentInfoArts
        exclude = ['student']
        widgets = {'guardian': forms.Select(attrs={'id': 'id_guardian'})}

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('guardian') == 'Other':
            for name in ('guardian_name_english', 'guardian_date_of_birth', 'guardian_nid', 'guardian_mobile'):
                if not cleaned.get(name):
                    self.add_error(name, "This field is required when guardian is 'Other'.")
        return cleaned

class AddressArtsForm(forms.ModelForm):
    class Meta:
        model = AddressArts
        exclude = ['student']
        widgets = {'permanent_address_same': forms.CheckboxInput(attrs={'id': 'id_copy_address'})}

class AcademicInformationArtsForm(forms.ModelForm):
    compulsorySubjects = forms.ModelMultipleChoiceField(queryset=HscArtsCompulsorySubjects.objects.filter(is_active=True), widget=forms.CheckboxSelectMultiple(attrs={'disabled': 'disabled'}), required=False)
    optionalSubjects = forms.ModelMultipleChoiceField(queryset=HscArtsOptionalSubjects.objects.filter(is_active=True), widget=forms.CheckboxSelectMultiple(attrs={'disabled': 'disabled'}), required=False)
    mainSubjects = forms.ModelChoiceField(queryset=HscArtsMainSubjects.objects.filter(is_active=True), widget=forms.RadioSelect(), required=False)
    FourSubjects = forms.ModelChoiceField(queryset=HscArtsFourthSubjects.objects.filter(is_active=True), widget=forms.RadioSelect(), required=False)

    class Meta:
        model = AcademicInformationArts
        exclude = ['student']
        widgets = {'ssc_session': forms.Select(attrs={'class': 'form-select'}), 'ssc_board': forms.Select(attrs={'class': 'form-select'}), 'ssc_year': forms.Select(attrs={'class': 'form-select'})}

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('mainSubjects') == cleaned_data.get('FourSubjects'):
            self.add_error('FourSubjects', 'The 4th subject cannot be the same as the main subject.')
        return cleaned_data

class PaymentArtsForm(forms.ModelForm):
    payment_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = PaymentArts
        exclude = ['student']
        widgets = {'amount': forms.NumberInput(attrs={'readonly': 'readonly'})}

    def __init__(self, *args, **kwargs):
        hsc_session = kwargs.pop('hsc_session', None)
        super().__init__(*args, **kwargs)
        self.fields['amount'].initial = hsc_session.fee.amount if hsc_session and hsc_session.fee else HscFeeType.objects.filter(fee_type__iexact='Admission').first().amount if HscFeeType.objects.filter(fee_type__iexact='Admission').exists() else 0

# ------------- Commerce Forms -------------
class HscAdmissionCommerceForm(forms.ModelForm):
    birthdate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True, label="Date of Birth")
    class Meta:
        model = HscAdmissionCommerce
        exclude = ['type', 'program']

class ParentInfoCommerceForm(forms.ModelForm):
    fathers_date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    mothers_date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    guardian_date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = ParentInfoCommerce
        exclude = ['student']
        widgets = {'guardian': forms.Select(attrs={'id': 'id_guardian'})}

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('guardian') == 'Other':
            for name in ('guardian_name_english', 'guardian_date_of_birth', 'guardian_nid', 'guardian_mobile'):
                if not cleaned.get(name):
                    self.add_error(name, "This field is required when guardian is 'Other'.")
        return cleaned

class AddressCommerceForm(forms.ModelForm):
    class Meta:
        model = AddressCommerce
        exclude = ['student']
        widgets = {'permanent_address_same': forms.CheckboxInput(attrs={'id': 'id_copy_address'})}

class AcademicInformationCommerceForm(forms.ModelForm):
    compulsorySubjects = forms.ModelMultipleChoiceField(queryset=HscCommerceCompulsorySubjects.objects.filter(is_active=True), widget=forms.CheckboxSelectMultiple(attrs={'disabled': 'disabled'}), required=False)
    optionalSubjects = forms.ModelMultipleChoiceField(queryset=HscCommerceOptionalSubjects.objects.filter(is_active=True), widget=forms.CheckboxSelectMultiple(attrs={'disabled': 'disabled'}), required=False)
    mainSubjects = forms.ModelChoiceField(queryset=HscCommerceMainSubjects.objects.filter(is_active=True), widget=forms.RadioSelect(), required=False)
    FourSubjects = forms.ModelChoiceField(queryset=HscCommerceFourthSubjects.objects.filter(is_active=True), widget=forms.RadioSelect(), required=False)

    class Meta:
        model = AcademicInformationCommerce
        exclude = ['student']
        widgets = {'ssc_session': forms.Select(attrs={'class': 'form-select'}), 'ssc_board': forms.Select(attrs={'class': 'form-select'}), 'ssc_year': forms.Select(attrs={'class': 'form-select'})}

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('mainSubjects') == cleaned_data.get('FourSubjects'):
            self.add_error('FourSubjects', 'The 4th subject cannot be the same as the main subject.')
        return cleaned_data

class PaymentCommerceForm(forms.ModelForm):
    payment_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = PaymentCommerce
        exclude = ['student']
        widgets = {'amount': forms.NumberInput(attrs={'readonly': 'readonly'})}

    def __init__(self, *args, **kwargs):
        hsc_session = kwargs.pop('hsc_session', None)
        super().__init__(*args, **kwargs)
        self.fields['amount'].initial = hsc_session.fee.amount if hsc_session and hsc_session.fee else HscFeeType.objects.filter(fee_type__iexact='Admission').first().amount if HscFeeType.objects.filter(fee_type__iexact='Admission').exists() else 0
