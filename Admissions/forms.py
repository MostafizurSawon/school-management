from django import forms
from .models import HscAdmissionScience, ParentInfo, Address, AcademicInformation, Payment, HscScienceSubjects

# class HscSessionForm(forms.ModelForm):
#     class Meta:
#         model = HscSession
#         fields = ['__all__']
#         widgets = {
#             'session_name': forms.TextInput(attrs={'class': 'form-control'})
#         }

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

    # <-- make this optional at the field-level!
    guardian_date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )

    class Meta:
        model = ParentInfo
        exclude = ['student']
        widgets = {
            # so our JS toggle can find it
            'guardian': forms.Select(attrs={'id': 'id_guardian'}),
        }

    def clean(self):
        cleaned = super().clean()
        guardian = cleaned.get('guardian')

        # only *then* require the four extras
        if guardian == 'Other':
            for name in (
                'guardian_name_english',
                'guardian_date_of_birth',   # now required=False above
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
            # give the checkbox its own id for JS
            'permanent_address_same': forms.CheckboxInput(attrs={'id': 'id_copy_address'}),
        }



class AcademicInformationForm(forms.ModelForm):
    class Meta:
        model = AcademicInformation
        exclude = ['student']
        widgets = {
          'ssc_session': forms.Select(attrs={'class':'form-control'}),
        }




class PaymentForm(forms.ModelForm):
    payment_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    class Meta:
        model = Payment
        exclude = ['student']