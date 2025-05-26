from django.shortcuts import get_object_or_404, render, redirect
from core.form import DiagnosticForm
from core.models import Diagnostic, Vehicule

################################################################################

# def diagnostic_list(request):
#     diagnostics = Diagnostic.objects.filter(utilisateur=request.user)
#     return render(request, 'diagnostics/list.html', {'diagnostics': diagnostics})  

def diagnostic_list_par_vehicule(request, vehicule_id):
    vehicule = get_object_or_404(Vehicule, pk=vehicule_id, utilisateur=request.user)
    diagnostics = Diagnostic.objects.filter(vehicule=vehicule)

    paginator = Paginator(diagnostics, 5)  # 5 diagnostics par page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'diagnostics/list.html', {
        'vehicule': vehicule,
        'page_obj': page_obj
    })

def diagnostic_detail(request, pk):
    diagnostic = get_object_or_404(Diagnostic, pk=pk)
    return render(request, 'diagnostics/detail.html', {'diagnostic': diagnostic})

def diagnostic_create(request, vehicule_id):
    vehicule = get_object_or_404(Vehicule, pk=vehicule_id)
    form = DiagnosticForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        diagnostic = form.save(commit=False)
        diagnostic.vehicule = vehicule
        diagnostic.save()
        return redirect('diagnostic_list_par_vehicule', vehicule_id=vehicule.id)
    return render(request, 'diagnostics/form.html', {'form': form, 'vehicule':vehicule})

def diagnostic_update(request, pk):
    diagnostic = get_object_or_404(Diagnostic, pk=pk)
    form = DiagnosticForm(request.POST or None, request.FILES or None, instance=diagnostic)
    if form.is_valid():
        form.save()
        return redirect('diagnostic_detail', pk=pk)
    return render(request, 'diagnostics/form.html', {'form': form, 'diagnostic':diagnostic})

def diagnostic_delete(request, pk):
    diagnostic = get_object_or_404(Diagnostic, pk=pk)
    if request.method == 'POST':
        diagnostic.delete()
        return redirect('diagnostic_list_par_vehicule', vehicule_id=diagnostic.vehicule.id)
    return render(request, 'diagnostics/confirm_delete.html', {'diagnostic': diagnostic})

def diagnostic_delete_file(request, pk):
    diagnostic = get_object_or_404(Diagnostic, pk=pk)
    if diagnostic.fichier:
        # Supprimer le fichier du disque
        diagnostic.fichier.delete(save=False)
        # Nettoyer le champ
        diagnostic.fichier = None
        diagnostic.save()
    return redirect('diagnostic_detail', pk=pk)

def diagnostic_update_file(request, pk):
    diagnostic = get_object_or_404(Diagnostic, pk=pk)
    if request.method == 'POST' and request.FILES.get('fichier'):
        # Supprimer l’ancien fichier
        if diagnostic.fichier:
            diagnostic.fichier.delete(save=False)
        # Enregistrer le nouveau
        diagnostic.fichier = request.FILES['fichier']
        diagnostic.save()
    return redirect('diagnostic_detail', pk=pk)