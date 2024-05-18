from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from .forms import UserForm, UserProfileForm

def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('login')  
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'registration/register.html', {'user_form': user_form, 'profile_form': profile_form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('home')  
            else:
                return HttpResponse("Tu cuenta está desactivada.")
        else:
            return HttpResponse("Datos de inicio de sesión inválidos.")
    else:
        return render(request, 'registration/login.html', {})

def home(request):
    return render(request, 'home.html', {})
