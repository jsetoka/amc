
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        labels = {
            'username': "Nom d'utilisateur",
            'password1': "Mot de passe",
            'password2': "Confirmation du mot de passe",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Personnalisation des attributs HTML
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "Entrez votre nom d'utilisateur"
        })

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "Entrez votre mot de passe"
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "Confirmez votre mot de passe"
        })

        # Personnalisation des labels
        self.fields['username'].label = "Nom d'utilisateur "
        self.fields['password1'].label = "Mot de passe "
        self.fields['password2'].label = "Confirmation du mot de passe "



from core.models import Vehicule, Abonnement, Diagnostic, Paiement, Protocole
class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicule
        fields = ['utilisateur', 'marque', 'modele', 'numero_chassis','annee']


# class AbonnementForm(forms.ModelForm):
#     class Meta:
#         model = Abonnement
#         fields = ['vehicule', 'type', 'actif']

class AbonnementForm(forms.ModelForm):
    METHODE_CHOIX = [
        ('mtn', 'MTN Money'),
        ('airtel', 'Airtel Money'),
        ('especes', 'Espèces'),
    ]
    methode_paiement = forms.ChoiceField(
        choices=METHODE_CHOIX,
        widget=forms.RadioSelect,
        required=False,
        label="Méthode de paiement"
    )

    phone = forms.CharField(
        required=False,
        label="Numéro MTN MoMo",
        widget=forms.TextInput(attrs={
            "placeholder": "Ex : 24206XXXXXX"
        })
    )

    class Meta:
        model = Abonnement
        fields = ['type', 'vehicule', 'actif']  # ou selon ton modèle

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # récupère l'utilisateur transmis
        super().__init__(*args, **kwargs)
        if user:
            self.fields['vehicule'].queryset = Vehicule.objects.filter(utilisateur=user)
   
    def clean(self):
        cleaned_data = super().clean()
        methode = cleaned_data.get("methode_paiement")
        phone = cleaned_data.get("phone")

        if methode == "mtn" and not phone:
            self.add_error("phone", "Le numéro MTN MoMo est requis pour ce mode de paiement.")
        if methode == "airtel" and not phone:
            self.add_error("phone", "Le numéro Airtel Money est requis pour ce mode de paiement.")


class PaiementForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = ['abonnement','montant', 'methode', 'statut']


class DiagnosticForm(forms.ModelForm):
    class Meta:
        model = Diagnostic
        fields = ['fichier']


class ProtocoleForm(forms.ModelForm):
    class Meta:
        model = Protocole
        fields = ['fichier']