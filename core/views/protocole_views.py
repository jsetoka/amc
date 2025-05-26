from django.shortcuts import get_object_or_404, render, redirect
from core.form import DiagnosticForm, PaiementForm, ProtocoleForm, DiagnosticForm, VehicleForm, AbonnementForm
from core.models import Protocole
################################################################################


# def protocole_list(request):
#     protocoles = Diagnostic.objects.filter(utilisateur=request.user)
#     return render(request, 'protocoles/list.html', {'protocoles': protocoles})  

def protocole_list_par_diagnostic(request, diagnostic_id):
    diagnostic = get_object_or_404(Diagnostic, pk=diagnostic_id)
    protocoles = Protocole.objects.filter(diagnostic=diagnostic)
    return render(request, 'protocoles/list.html', {
        'diagnostic': diagnostic,
        'protocoles': protocoles
    })

def protocole_detail(request, pk):
    protocole = get_object_or_404(Protocole, pk=pk)
    return render(request, 'protocoles/detail.html', {'protocole': protocole})

def protocole_create(request, diagnostic_id):
    diagnostic = get_object_or_404(Diagnostic, pk=diagnostic_id)
    form = ProtocoleForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        protocole = form.save(commit=False)
        protocole.diagnostic = diagnostic
        protocole.save()
        diagnostic.status="Traité"
        diagnostic.save()
        return redirect('protocole_list_par_diagnostic', diagnostic_id=diagnostic.id)
    return render(request, 'protocoles/form.html', {'form': form, 'diagnostic':diagnostic})

def protocole_update(request, pk):
    protocole = get_object_or_404(Protocole, pk=pk)
    form = DiagnosticForm(request.POST or None, request.FILES or None, instance=protocole)
    if form.is_valid():
        form.save()
        # protocole.diagnostic.status="Traité"
        # protocole.diagnostic.save()
        return redirect('protocole_detail', pk=pk)
    return render(request, 'protocoles/form.html', {'form': form, 'protocole':protocole})

def protocole_delete(request, pk):
    protocole = get_object_or_404(Protocole, pk=pk)
    if request.method == 'POST':
        protocole.delete()
        return redirect('protocole_list_par_diagnostic', diagnostic_id=protocole.diagnostic.id)
    return render(request, 'protocoles/confirm_delete.html', {'protocole': protocole})

def protocole_delete_file(request, pk):
    protocole = get_object_or_404(Protocole, pk=pk)
    if protocole.fichier:
        # Supprimer le fichier du disque
        protocole.fichier.delete(save=False)
        # Nettoyer le champ
        protocole.fichier = None
        protocole.save()
    return redirect('protocole_detail', pk=pk)

def protocole_update_file(request, pk):
    protocole = get_object_or_404(Protocole, pk=pk)
    if request.method == 'POST' and request.FILES.get('fichier'):
        # Supprimer l’ancien fichier
        if protocole.fichier:
            protocole.fichier.delete(save=False)
        # Enregistrer le nouveau
        protocole.fichier = request.FILES['fichier']
        protocole.save()
    return redirect('protocole_detail', pk=pk)
