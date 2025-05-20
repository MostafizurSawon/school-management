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

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['notice_title', 'date', 'notice_description', 'notice_file']

