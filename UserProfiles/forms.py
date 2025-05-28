from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import SiteSettings, Notice


class RegistrationForm(UserCreationForm):
  first_name = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
  last_name = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
  usable_password = None

  class Meta:
      model = User
      fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
      # fields = '__all__'


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = '__all__'
        widgets = {
            'institution_name': forms.TextInput(attrs={
                'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500'
            }),
            'institution_description': forms.TextInput(attrs={
                'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500'
            }),
            'footer': forms.TextInput(attrs={
                'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500'
            }),
            'address': forms.Textarea(attrs={
                'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500',
                'rows': 3
            }),
            'mobile_number': forms.TextInput(attrs={
                'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500'
            }),
            'website': forms.URLInput(attrs={
                'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500'
            }),
            'logo': forms.ClearableFileInput(attrs={
                'class': 'file-input w-full'
            }),
            'favicon': forms.ClearableFileInput(attrs={
                'class': 'file-input w-full'
            }),
        }

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['notice_title', 'date', 'notice_file']
        widgets = {
            'notice_title': forms.TextInput(attrs={
                'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500'
            }),
            'date': forms.DateInput(attrs={
                'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500',
                'type': 'date'
            }),
            'notice_file': forms.ClearableFileInput(attrs={
                'class': 'file-input w-full'
            }),
        }

