from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from core.form import PaiementForm
from core.models import Paiement, Abonnement
from core.utils.momopay import paymentstatus
from dateutil.relativedelta import relativedelta
from datetime import date

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

def paiement_en_cours(request, abonnement_id):
    abonnement = get_object_or_404(Abonnement, id=abonnement_id)
    return render(request, 'paiements/paiement_en_cours.html', {'abonnement': abonnement})

def verifier_paiement(request, abonnement_id):
    try:
        abonnement = Abonnement.objects.get(id=abonnement_id)

        # Ne pas réappeler si déjà payé
        if abonnement.actif:
            return JsonResponse({'status': 'SUCCESSFUL'})

        # Appel API pour voir si le paiement a abouti
        res = paymentstatus(abonnement.apiuser, abonnement.token)
        reponse = res.json()
        statut = reponse.get('status')

        if statut == 'SUCCESSFUL':
            abonnement.actif = True
            abonnement.statut_paiement = 'SUCCESSFUL'
            abonnement.date_fin = date.today() + relativedelta(months=abonnement.type.duree)
            abonnement.save()

            # Enregistrement du paiement
            Paiement.objects.create(
                abonnement=abonnement,
                montant=abonnement.type.montant,
                methode="MTN Money",
                statut="SUCCESSFUL"
            )
        elif statut == 'FAILED':
            abonnement.statut_paiement = 'FAILED'
            abonnement.save()

        return JsonResponse({'status': statut})

    except Abonnement.DoesNotExist:
        return JsonResponse({'status': 'ERROR'})
    
