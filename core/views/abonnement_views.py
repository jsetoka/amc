from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from core.form import AbonnementForm
from core.models import Abonnement, Vehicule, Paiement
from core.utils.momopay import requesttopay
from django.core.paginator import Paginator


################################################################################

def abonnement_list_par_vehicule(request, vehicule_id):
    vehicule = get_object_or_404(Vehicule, pk=vehicule_id, utilisateur=request.user)
    abonnements = Abonnement.objects.filter(vehicule=vehicule).order_by('-date_debut')
    paginator = Paginator(abonnements, 10 )  # 5 abonnements par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    titre = 'Les abonnements du véhicule ' + vehicule.marque + ' ' + vehicule.modele + ' - ' + vehicule.numero_chassis
    return render(request, 'abonnements/list.html', {
        'titre':titre,
        'abonnements': page_obj,
        'page_obj': page_obj
    })

def abonnement_list(request):
    abonnements = Abonnement.objects.filter(utilisateur=request.user)
    paginator = Paginator(abonnements, 10 )  # 5 abonnements par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    titre = 'Mes abonnements'
    return render(request, 'abonnements/list.html', {
      'titre':titre,
      'abonnements': page_obj,
      'page_obj': page_obj
    })  

def abonnement_detail(request, pk):
    abonnements = get_object_or_404(Abonnement, pk=pk, utilisateur=request.user)
    return render(request, 'abonnements/detail.html', {'abonnements': abonnements})

@login_required
def abonnement_create(request):
    form = AbonnementForm(request.POST or None, user=request.user)
    if form.is_valid():
        phone = request.POST.get("phone")
        abonnement = form.save(commit=False)
        abonnement.utilisateur = request.user
        methode = form.cleaned_data['methode_paiement']
        abonnement.save()  # ⏳ On sauve même en attente

        if methode == 'mtn':
            montant = str(abonnement.type.montant)
            res = requesttopay(montant, "242"+ phone, "Payer Message", "Note")
            if res and res.get('status_code') == 202:
                # Sauvegarde des infos pour vérification ultérieure
                abonnement.apiuser = res.get('apiuser')
                abonnement.token = res.get('token')
                abonnement.montant = abonnement.type.montant
                abonnement.statut_paiement = 'PENDING'
                abonnement.save()
                
                return redirect('paiement_en_cours', abonnement_id=abonnement.id)
        if methode == 'airtel':
            montant = str(abonnement.type.montant)
            res = requesttopay(montant, "242"+ phone, "Payer Message", "Note")
            if res and res.get('status_code') == 202:
                # Sauvegarde des infos pour vérification ultérieure
                abonnement.apiuser = res.get('apiuser')
                abonnement.token = res.get('token')
                abonnement.montant = abonnement.type.montant
                abonnement.statut_paiement = 'PENDING'
                abonnement.save()
                
                return redirect('paiement_en_cours', abonnement_id=abonnement.id)
        if methode == 'especes':
            # Sauvegarde des infos pour vérification ultérieure
            abonnement.apiuser = ''
            abonnement.token = ''
            abonnement.montant = abonnement.type.montant
            abonnement.statut_paiement = 'PENDING'
            abonnement.save()
            Paiement.objects.create(
              abonnement=abonnement,
              montant=abonnement.type.montant,
              methode="Espèces",
              statut="PENDING"
            )      
            return redirect('paiement_en_attente', abonnement_id=abonnement.id)
    form.initial['utilisateur'] = request.user
    return render(request, 'abonnements/create.html', {'form': form})


def abonnement_update(request, pk):
    abonnement = get_object_or_404(Abonnement, pk=pk, utilisateur=request.user)
    form = AbonnementForm(request.POST or None, instance=abonnement)
    if form.is_valid():
        form.save()
        return redirect('abonnement_list')
    return render(request, 'abonnements/form.html', {'form': form, 'abonnement':abonnement})

def abonnement_delete(request, pk):
    abonnement = get_object_or_404(Abonnement, pk=pk, utilisateur=request.user)
    if request.method == 'POST':
        abonnement.delete()
        return redirect('abonnement_list')
    return render(request, 'abonnements/confirm_delete.html', {'abonnement': abonnement})

