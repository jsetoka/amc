from django.contrib import admin

# Register your models here.
from .models import Vehicule, Abonnement, Paiement, Diagnostic, Protocole, TypeAbonnement, Message, Rendezvous

admin.site.register(Vehicule)
admin.site.register(Abonnement)
admin.site.register(TypeAbonnement)
admin.site.register(Paiement)
admin.site.register(Diagnostic)
admin.site.register(Protocole)
admin.site.register(Message)
admin.site.register(Rendezvous)

admin.site.site_header = "AM Consulting"
admin.site.site_title = "AMC - Administration"
admin.site.index_title = "Tableau de bord de AMC"
