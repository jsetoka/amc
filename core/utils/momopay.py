##########################################################
# API MOMO
##########################################################
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import json, base64
import uuid
import requests

from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404

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
    try:
        if response.status_code == 200:
            token_data = response.json()
            token_str = token_data.get("access_token")  # ou "token", selon l'API
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

