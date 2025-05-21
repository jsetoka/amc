from django.contrib import admin

# Register your models here.
from .models import Vehicule, Abonnement, Paiement, Diagnostic, Protocole, TypeAbonnement

admin.site.register(Vehicule)
admin.site.register(Abonnement)
admin.site.register(TypeAbonnement)
admin.site.register(Paiement)
admin.site.register(Diagnostic)
admin.site.register(Protocole)
