import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import UserForm, UserProfileForm
from django.core.files.storage import FileSystemStorage
from .models import UserProfile
from .utils import execute_ssh_commands, sftp_upload_file

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

            password = user_form.cleaned_data['password']
            commands = [
                f'sudo useradd -m {user.username}',
                f'echo "{user.username}:{password}" | sudo chpasswd',
                f'sudo usermod -aG ftpusers {user.username}',
                f'sudo mkdir -p /home/{user.username}/ftp/files',
                f'sudo chown -R {user.username}:ftpusers /home/{user.username}',
                f'sudo chmod 750 /home/{user.username}/ftp',
                f'sudo chmod 750 /home/{user.username}/ftp/files'
            ]

            key_filepath = '/home/debian/.ssh/id_rsa'

            try:
                execute_ssh_commands(
                    hostname=settings.FTP_SERVER_IP,
                    port=22,
                    username='debian',
                    key_filepath=key_filepath,
                    commands=commands
                )
                return redirect('login')
            except Exception as e:
                print(f"Failed to execute commands via SSH: {e}")
                user.delete()
                profile.delete()
                return render(request, 'registration/register.html', {
                    'user_form': user_form,
                    'profile_form': profile_form,
                    'error': str(e)
                })
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

@login_required
def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        upload = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(upload.name, upload)
        uploaded_file_path = fs.path(filename)

        remote_path = f'/home/{request.user.username}/ftp/files/{filename}'

        # Assuming the password is entered in a field in the upload form
        password = request.POST.get('password')

        try:
            sftp_upload_file(
                hostname=settings.FTP_SERVER_IP,
                port=22,
                username=request.user.username,
                password=password,
                local_path=uploaded_file_path,
                remote_path=remote_path
            )
        except Exception as e:
            print(f"Failed to upload file via SFTP: {e}")

        fs.delete(filename)

        return redirect('home')
    return render(request, 'home.html')
