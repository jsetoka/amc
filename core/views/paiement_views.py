from django.shortcuts import get_object_or_404, render, redirect
from core.form import PaiementForm
from core.models import Paiement

################################################################################
def paiement_list_par_abonnement(request, abonnement_id):
    abonnement = get_object_or_404(Abonnement, pk=abonnement_id)
    paiements = Paiement.objects.filter(abonnement=abonnement)
    return render(request, 'paiements/list.html', {
        'abonnement': abonnement,
        'paiements': paiements
    })

def paiement_list(request, pk):
    paiements = Paiement.objects.filter(pk=pk)
    return render(request, 'paiements/list.html', {'paiements': paiements})  

def paiement_detail(request, pk):
    paiements = get_object_or_404(Paiement, pk=pk)
    return render(request, 'paiements/detail.html', {'paiements': paiements})

def paiement_create(request, abonnement_id):
    abonnement = get_object_or_404(Abonnement, pk=abonnement_id)
    form = PaiementForm(request.POST or None)
    if form.is_valid():
        paiement = form.save(commit=False)
        paiement.abonnement = abonnement
        paiement.save()
        return redirect('paiement_list_par_abonnement', abonnement_id=abonnement.id)
    form.initial['abonnement'] = abonnement
    return render(request, 'paiements/form.html', {'form': form})

def paiement_update(request, pk):
    paiement = get_object_or_404(Paiement, pk=pk)
    form = PaiementForm(request.POST or None, instance=paiement)
    if form.is_valid():
        form.save()
        return redirect('paiement_list_par_abonnement', abonnement_id=paiement.abonnement.id)
    return render(request, 'paiements/form.html', {'form': form})

def paiement_delete(request, pk):
    paiement = get_object_or_404(Paiement, pk=pk)
    abonnement = get_object_or_404(Abonnement, pk=paiement.abonnement_id)
    if request.method == 'POST':
        paiement.delete()
        return redirect('paiement_list_par_abonnement', abonnement_id=abonnement.id)
    return render(request, 'paiements/confirm_delete.html', {'paiement': paiement})

