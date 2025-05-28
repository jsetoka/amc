from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from core.form import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def is_client(user):
    return user.groups.filter(name='Client').exists()


def inscription(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # ou 'dashboard'
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def connexion(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.POST.get('next') or '/'
            return redirect(next_url)
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, 'registration/login.html', {'form': form})

def deconnexion(request):
    logout(request)
    return redirect('login')


@login_required
def profile(request):
    return render(request, 'registration/profile.html', {'user': request.user})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # pour éviter de déconnecter l'utilisateur
            messages.success(request, 'Votre mot de passe a été mis à jour avec succès.')
            return redirect('password_change_done')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = PasswordChangeForm(user=request.user)
    
    return render(request, 'registration/change_password.html', {'form': form})

@login_required
def password_change_done(request):
    return render(request, 'registration/password_change_done.html')
