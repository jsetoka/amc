
# Create your models here.
from django.db import models
from django.contrib.humanize.templatetags.humanize import intcomma

# Create your models here.
from django.contrib.auth.models import User

class Vehicule(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    annee = models.PositiveIntegerField()
    numero_chassis = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.marque} {self.modele} ({self.numero_chassis})"

    
class TypeAbonnement(models.Model):
    montant = models.DecimalField(max_digits=8, decimal_places=2)
    type = models.CharField(max_length=20, choices=[('annuel', 'Annuel'), ('trimestriel', 'Trimestriel'), ('mensuel', 'Mensuel')])
    duree = models.PositiveIntegerField()

    def __str__(self):
        montant = intcomma(int(self.montant))
        return f"{self.type} - {montant}"
    
class Abonnement(models.Model):
    METHODE_CHOIX = [
        ('mtn', 'MTN Money'),
        ('airtel', 'Airtel Money'),
        ('especes', 'Espèces'),
    ]
    
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(TypeAbonnement, on_delete=models.CASCADE)
    date_debut = models.DateField(auto_now_add=True)
    date_fin = models.DateField(blank=True, null=True)  # ✅ nouveau champ
    montant = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    actif = models.BooleanField(default=False)
    apiuser = models.CharField(max_length=100, blank=True, null=True)
    token = models.TextField(blank=True, null=True)
    statut_paiement = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Abonnement {self.type} - {self.utilisateur.username}"


class Paiement(models.Model):
    abonnement = models.OneToOneField(Abonnement, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    methode = models.CharField(max_length=20)
    statut = models.CharField(max_length=20)

    def __str__(self):
        return f"Paiement {self.montant:.0f} - {self.methode} ({self.statut})"

class Diagnostic(models.Model):
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)
    fichier = models.FileField(upload_to='media/diagnostics/')
    date_envoi = models.DateTimeField(auto_now_add=True)
    etat = models.CharField(max_length=20, choices=[('INIT', 'Initialisé'), ('PENDING', 'En cours'), ('DONE', 'Terminé')])

    def __str__(self):
        return f"Diagnostic de {self.vehicule} - {self.etat}"

class Protocole(models.Model):
    diagnostic = models.OneToOneField(Diagnostic, on_delete=models.CASCADE)
    fichier = models.FileField(upload_to='protocoles/')
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Protocole pour {self.diagnostic.vehicule}"

class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    fichier = models.FileField(upload_to="chat_files/", blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='reponses')  # ✅


    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.username} → {self.recipient.username} : {self.content[:30]}"
