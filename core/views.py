from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from dateutil.relativedelta import relativedelta
from datetime import date

from core.models import Vehicule, Abonnement, Diagnostic, Paiement
from diag import settings

from .form import CustomUserCreationForm


def is_client(user):
    return user.groups.filter(name='Client').exists()

def index(request):
    return render(request, 'accueil.html')

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
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate (request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    return render(request, 'registration/login.html')

def deconnexion(request):
    logout(request)
    return redirect('login')



################################################################################
from django.shortcuts import get_object_or_404
from core.form import VehicleForm


def vehicle_list(request):
    vehicles = Vehicule.objects.filter(utilisateur=request.user)
    return render(request, 'vehicules/list.html', {'vehicles': vehicles})  

#@user_passes_test(is_client, login_url='login')
def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicule, pk=pk, utilisateur=request.user)
    return render(request, 'vehicules/detail.html', {'vehicle': vehicle})


def vehicle_create(request):
    form = VehicleForm(request.POST or None)
    if form.is_valid():
        vehicle = form.save(commit=False)
        vehicle.utilisateur = request.user
        vehicle.save()
        return redirect('vehicle_list')
    form.initial['utilisateur'] = request.user
    return render(request, 'vehicules/form.html', {'form': form})

def vehicle_update(request, pk):
    vehicle = get_object_or_404(Vehicule, pk=pk, utilisateur=request.user)
    form = VehicleForm(request.POST or None, instance=vehicle)
    if form.is_valid():
        form.save()
        return redirect('vehicle_detail', pk=pk)
    return render(request, 'vehicules/form.html', {'form': form})

def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicule, pk=pk, utilisateur=request.user)
    if request.method == 'POST':
        vehicle.delete()
        return redirect('vehicle_list')
    return render(request, 'vehicules/confirm_delete.html', {'vehicle': vehicle})

################################################################################
from django.shortcuts import get_object_or_404
from core.form import AbonnementForm

def abonnement_list_par_vehicule(request, vehicule_id):
    vehicule = get_object_or_404(Vehicule, pk=vehicule_id, utilisateur=request.user)
    abonnements = Abonnement.objects.filter(vehicule=vehicule)
    return render(request, 'abonnements/list.html', {
        'vehicule': vehicule,
        'abonnements': abonnements
    })

def abonnement_list(request):
    abonnements = Abonnement.objects.filter(utilisateur=request.user)
    return render(request, 'abonnements/list.html', {'abonnements': abonnements})  

def abonnement_detail(request, pk):
    abonnements = get_object_or_404(Abonnement, pk=pk, utilisateur=request.user)
    return render(request, 'abonnements/detail.html', {'abonnements': abonnements})

# def abonnement_create(request):
#     form = AbonnementForm(request.POST or None, user=request.user)
#     if form.is_valid():
#         abonnement = form.save(commit=False)
#         abonnement.utilisateur = request.user
#         methode = form.cleaned_data['methode_paiement']
#         if methode == 'mtn':
#             montant=str(abonnement.type.montant)
#             res = requesttopay(montant, "242065091111", "Payer Message", "Note")

#             if (res['status_code']==202):
#                 apiuser = res.get('apiuser')
#                 token = res.get('token')
#                 res2 = paymentstatus(apiuser, token)
#                 reponse=res2.json()
#                 print(reponse)
#                 if (reponse.get('status')=='SUCCESSFUL'):
#                     abonnement.actif=True
#                     abonnement.date_fin = date.today() + relativedelta(months=abonnement.type.duree)
#                     abonnement.save()

#                     # ✅ Enregistrement du paiement
#                     Paiement.objects.create(
#                         abonnement=abonnement,
#                         montant=abonnement.type.montant,
#                         methode="MTN Money",
#                         statut="SUCCESSFUL"
#                     )
#         return redirect('abonnement_list')
#     form.initial['utilisateur'] = request.user
#     return render(request, 'abonnements/create.html', {'form': form})


def abonnement_create(request):
    form = AbonnementForm(request.POST or None, user=request.user)
    if form.is_valid():
        abonnement = form.save(commit=False)
        abonnement.utilisateur = request.user
        methode = form.cleaned_data['methode_paiement']
        abonnement.save()  # ⏳ On sauve même en attente

        if methode == 'mtn':
            montant = str(abonnement.type.montant)
            res = requesttopay(montant, "242065091111", "Payer Message", "Note")

            if res.get('status_code') == 202:
                # Sauvegarde des infos pour vérification ultérieure
                abonnement.apiuser = res.get('apiuser')
                abonnement.token = res.get('token')
                abonnement.statut_paiement = 'PENDING'
                abonnement.save()
                
                return redirect('paiement_en_cours', abonnement_id=abonnement.id)
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


################################################################################
from django.shortcuts import get_object_or_404
from core.form import PaiementForm


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



################################################################################
from django.shortcuts import get_object_or_404
from core.form import DiagnosticForm


# def diagnostic_list(request):
#     diagnostics = Diagnostic.objects.filter(utilisateur=request.user)
#     return render(request, 'diagnostics/list.html', {'diagnostics': diagnostics})  

def diagnostic_list_par_vehicule(request, vehicule_id):
    vehicule = get_object_or_404(Vehicule, pk=vehicule_id, utilisateur=request.user)
    diagnostics = Diagnostic.objects.filter(vehicule=vehicule)
    return render(request, 'diagnostics/list.html', {
        'vehicule': vehicule,
        'diagnostics': diagnostics
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



##########################################################
# API MOMO
##########################################################
from django.views.decorators.csrf import csrf_exempt
import json, base64
from django.http import JsonResponse
@csrf_exempt  # (à éviter en production, mieux : token CSRF)
def creer_utilisateur(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nom = data.get('nom')
        email = data.get('email')
        return JsonResponse({
            'message': f"Utilisateur {nom} enregistré avec l'email {email}.",
            'status': 'success'
        })
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)







import uuid
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def momopay(request, mp=""):
    return render(request, 'momopay.html')

def apiuser(url, reference_id, key):
    url = settings.URL_SITE + '/v1_0/apiuser/' + reference_id + '/apikey'
    headers = {
        "Cache-Control": "no-cache",
        "Ocp-Apim-Subscription-Key": key
    }
    params = {
        "X-Reference-Id": reference_id
    }    
    try:
        response = requests.post(url, headers=headers)
        try:
            data = response.json()
            apiKey = data["apiKey"]
            return apiKey
        except ValueError:
            data = {"raw_response": response.text}

        return JsonResponse(data, status=response.status_code)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



def apikey(url, reference_id, key):
    url = settings.URL_SITE + '/v1_0/apiuser/' + reference_id
    headers = {
        "Cache-Control": "no-cache",
        "Ocp-Apim-Subscription-Key": key
    }
    params = {
        "X-Reference-Id": reference_id
    }    
    try:
        response = requests.get(url, headers=headers, params=params)
        if (response.status_code==200):
            apiuser(url, reference_id, key)
        # JsonResponse(response)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def access_token(url, apiuser, apikey, oask):
    url = settings.URL_SITE + '/collection/token/'       

    auth_str = f"{apiuser}:{apikey}"
    auth_bytes = auth_str.encode('utf-8')
    token = base64.b64encode(auth_bytes).decode('utf-8')  # ← on re-décode le résultat en str lisible
    headers = {
        # "Cache-Control": "no-cache",
        "Content-Type": "application/json",
        "Authorization": 'Basic ' + token,
        "Ocp-Apim-Subscription-Key": oask
    }
    response = requests.post(url, headers=headers)
    print ('jojo',response.json())
    try:
        if response.status_code == 200:
            token_data = response.json()
            token_str = token_data.get("access_token")  # ou "token", selon l'API
            print ('sylva',token_str)
            return token_str
        else:
            return JsonResponse({"error": "Échec d'obtention du token", "details": response.text})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


#@csrf_exempt  # (à retirer en production ou remplacer par vérification CSRF)
def create_momo_user():
    reference_id = str(uuid.uuid4())
    key = settings.API_KEY_MOMO

    url = settings.URL_SITE + "/v1_0/apiuser"
    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "X-Reference-Id": reference_id,
        "Ocp-Apim-Subscription-Key": key
    }
    body = {
        "providerCallbackHost": "string"  # Ton URL callback
    }
    try:
        response = requests.post(url, json=body, headers=headers)
        if (response.status_code==201):
            apikey = apiuser(url, reference_id, key)
        else:
            apikey=""

        return ({'apiuser': reference_id, 'apikey': apikey})
    except Exception as e:
        return ({"error": str(e), "status":500})
    
    
def requesttopay(montant="1400", phone="242065091111", payermessage="Payer Message", payeenote="Note"):
    user = create_momo_user()
    url = settings.URL_SITE + "/collection/v1_0/requesttopay"
    oask=settings.API_KEY_MOMO
    apiuser=user.get('apiuser')
    apikey=user.get('apikey')
    token = access_token(url, apiuser, apikey, oask)

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
        #"X-Callback-Url": "",
        "X-Reference-Id": apiuser,
        "X-Target-Environment":"sandbox",
        "Ocp-Apim-Subscription-Key": oask
    }
    print(headers)
    body = {
        "amount": montant,
        "currency":"EUR",
        "externalId":apiuser,
        "payer": {
            "partyIdType":"MSISDN",
            "partyId":phone,
        },
        "payerMessage":payermessage,
        "payeeNote":payeenote,

    }

    try:
        response = requests.post(url, json=body, headers=headers)
        if (response.status_code==202):
            return ({"status_code":response.status_code, "apiuser": apiuser, "token":token })
    except Exception as e:
        return ({"error": str(e), "status":500})


def paymentstatus(apiuser, token):
    # transaction_id = data.get('transaction_id')
    oask=settings.API_KEY_MOMO
    url = settings.URL_SITE + "/collection/v1_0/requesttopay/" + apiuser
    headers = {
        "Authorization": 'Bearer ' + token,
        "X-Target-Environment":"sandbox",
        "Ocp-Apim-Subscription-Key": oask
    }
    body = {
    }
    try:
        response = requests.get(url, json=body, headers=headers)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    return response


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
    
def paiement_en_cours(request, abonnement_id):
    abonnement = get_object_or_404(Abonnement, id=abonnement_id)
    return render(request, 'abonnements/paiement_en_cours.html', {'abonnement': abonnement})