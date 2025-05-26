from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from core.form import DiagnosticForm, PaiementForm, ProtocoleForm, DiagnosticForm, VehicleForm, AbonnementForm
from django.contrib.auth import login, authenticate, logout
from core.form import CustomUserCreationForm
from diag import settings
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

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
