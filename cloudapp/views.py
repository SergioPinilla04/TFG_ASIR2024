from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import UserForm, UserProfileForm
from .utils import execute_ssh_command
from django.conf import settings

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

            # Define los comandos que necesitas ejecutar como root
            password = user_form.cleaned_data["password"]
            commands = [
                f'sudo useradd -m {user.username}',
                f'echo "{user.username}:{password}" | sudo chpasswd',
                f'sudo mkdir /home/{user.username}/ftp',
                f'sudo chown nobody:nogroup /home/{user.username}/ftp',
                f'sudo chmod a-w /home/{user.username}/ftp',
                f'sudo mkdir /home/{user.username}/ftp/files',
                f'sudo chown -R {user.username}:{user.username} /home/{user.username}/ftp/files'
            ]

            # Ruta de la clave privada
            key_filepath = '/home/debian/.ssh/id_rsa'  # Asegúrate de que esta clave tiene permisos 600

            # Ejecutar los comandos via SSH
            for command in commands:
                execute_ssh_command(
                    hostname=settings.FTP_SERVER_IP,
                    port=22,  # puerto por defecto de SSH
                    username='debian',  # usuario con permisos sudo sin contraseña
                    key_filepath=key_filepath,
                    command=command
                )

            return redirect('login')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'registration/register.html', {'user_form': user_form, 'profile_form': profile_form})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid credentials'})
    return render(request, 'registration/login.html')

@login_required
def home(request):
    return render(request, 'home.html')

def logout(request):
    auth_logout(request)
    return redirect('login')
