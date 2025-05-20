from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import  AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login , update_session_auth_hash, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . import forms
from .models import SiteSettings
from .forms import SiteSettingsForm
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
def register(request):
    if request.method == 'POST':
        register_form = forms.RegistrationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request, 'Account Created Successfully! Login now!')
            return redirect('user_login')
    
    else:
        register_form = forms.RegistrationForm()
    return render(request, 'register.html', {'form' : register_form, 'type' : 'Register'})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['username']
            user_pass = form.cleaned_data['password']
            user = authenticate(username=user_name, password=user_pass)
            if user is not None:
                messages.success(request, 'Logged in Successfully')
                login(request, user)
                return redirect('profile')
            else:
                messages.warning(request, 'Login information incorrect')
                return redirect('register')
        else:
            return HttpResponse("Wrong Credentials!")
    else:
        form = AuthenticationForm()
        return render(request, 'register.html', {'form' : form, 'type' : 'Login'})


@login_required
def profile(request):
    context = {}

    if request.user.is_superuser:
        instance = SiteSettings.objects.first()
        if request.method == 'POST':
            form = SiteSettingsForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                form.save()
                messages.success(request, "Institution info updated successfully!")
                return redirect('profile')
        else:
            form = SiteSettingsForm(instance=instance)
        context['form'] = form

    return render(request, 'profile.html', context)


def user_logout(request):
    logout(request)
    return redirect('user_login')



@login_required
def site_settings_view(request):
    instance = SiteSettings.objects.first()
    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = SiteSettingsForm(instance=instance)

    return render(request, 'profile.html', {'form': form})
