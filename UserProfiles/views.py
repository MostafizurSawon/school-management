from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import  AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login , update_session_auth_hash, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . import forms
from .models import SiteSettings, Notice
from .forms import SiteSettingsForm, NoticeForm
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator

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


def user_logout(request):
    logout(request)
    return redirect('user_login')


@login_required
def profile(request):
    context = {}

    if request.user.is_superuser:
        site_instance = SiteSettings.objects.first()
        site_form = SiteSettingsForm(request.POST or None, request.FILES or None, instance=site_instance)

        if request.method == 'POST':
            if 'save_settings' in request.POST:
                if site_form.is_valid():
                    site_form.save()
                    messages.success(request, "Institution info updated successfully!")
                    return redirect('profile')

        context['site_settings_form'] = site_form

    return render(request, 'profile.html', context)

@login_required
def create_notice(request):
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')  # Adjust as needed

    form = NoticeForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Notice added successfully!")
            return redirect('portal-notice')

    return render(request, 'portal_notice.html', {'notice_form': form})



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
 
    return render(request, 'general_setting.html', {'form': form})


def notice_list(request):
    notices = Notice.objects.order_by('-date')  
    paginator = Paginator(notices, 5)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    start_index = (page_obj.number - 1) * paginator.per_page
    
    return render(request, 'base.html', {'page_obj': page_obj, 'start_index': start_index})

