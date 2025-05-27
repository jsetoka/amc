from django.urls import path
from django.contrib.auth import views as auth_views
from core.views import * 
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', dashboard_views.index, name="index"),
    path('accounts/login/', accounts_views.connexion, name='login'),
    path('accounts/signup/', accounts_views.inscription, name='signup'),
    path('accounts/logout/', accounts_views.deconnexion, name='logout'),
    path('accounts/profile/', accounts_views.profile, name='profile'),

 #   path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
 #   path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('mot-de-passe-oublie/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('mot-de-passe-envoye/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reinitialiser/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reinitialisation-terminee/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),


    path('vehicules/', vehicule_views.vehicle_list, name='vehicle_list'),
    path('vehicules/ajouter/', vehicule_views.vehicle_create, name='vehicle_create'),
    path('vehicules/<int:pk>/', vehicule_views.vehicle_detail, name='vehicle_detail'),
    path('vehicules/<int:pk>/modifier/', vehicule_views.vehicle_update, name='vehicle_update'),
    path('vehicules/<int:pk>/supprimer/', vehicule_views.vehicle_delete, name='vehicle_delete'),

    path('abonnements/', abonnement_views.abonnement_list, name='abonnement_list'),
    path('vehicules/<int:vehicule_id>/abonnements/', abonnement_views.abonnement_list_par_vehicule, name='abonnement_list_par_vehicule'),
    path('abonnements/ajouter/', abonnement_views.abonnement_create, name='abonnement_create'),
    path('abonnements/<int:pk>/', abonnement_views.abonnement_detail, name='abonnement_detail'),
    path('abonnements/<int:pk>/modifier/', abonnement_views.abonnement_update, name='abonnement_update'),
    path('abonnements/<int:pk>/supprimer/', abonnement_views.abonnement_delete, name='abonnement_delete'),

    #path('paiements/', views.paiement_list, name='paiement_list'),
    path('abonnements/<int:abonnement_id>/paiements/', paiement_views.paiement_list_par_abonnement, name='paiement_list_par_abonnement'),
    path('paiements/ajouter/<int:abonnement_id>', paiement_views.paiement_create, name='paiement_create'),
    path('paiements/<int:pk>/', paiement_views.paiement_detail, name='paiement_detail'),
    path('paiements/<int:pk>/modifier/', paiement_views.paiement_update, name='paiement_update'),
    path('paiements/<int:pk>/supprimer/', paiement_views.paiement_delete, name='paiement_delete'),
    path('paiement_en_cours/<int:abonnement_id>/', paiement_views.paiement_en_cours, name='paiement_en_cours'),
    path('paiement_en_attente/<int:abonnement_id>/', paiement_views.paiement_en_attente, name='paiement_en_attente'),
    path('api/verifier_paiement/<int:abonnement_id>/', paiement_views.verifier_paiement, name='verifier_paiement'),


    #path('diagnostics/', views.diagnostic_list, name='diagnostic_list'),
    path('vehicules/<int:vehicule_id>/diagnostics/', diagnostic_views.diagnostic_list_par_vehicule, name='diagnostic_list_par_vehicule'),
    path('diagnostics/ajouter/<int:vehicule_id>', diagnostic_views.diagnostic_create, name='diagnostic_create'),
    path('diagnostics/<int:pk>/', diagnostic_views.diagnostic_detail, name='diagnostic_detail'),
    path('diagnostics/<int:pk>/modifier/', diagnostic_views.diagnostic_update, name='diagnostic_update'),
    path('diagnostics/<int:pk>/supprimer/', diagnostic_views.diagnostic_delete, name='diagnostic_delete'),
    path('diagnostics/<int:pk>/supprimer-fichier/', diagnostic_views.diagnostic_delete_file, name='diagnostic_delete_file'),
    path('diagnostics/<int:pk>/modifier-fichier/', diagnostic_views.diagnostic_update_file, name='diagnostic_update_file'),

    #path('protocoles/', views.protocole_list, name='protocole_list'),
    path('diagnostics/<int:diagnostic_id>/protocoles/', protocole_views.protocole_list_par_diagnostic, name='protocole_list_par_diagnostic'),
    path('protocoles/ajouter/<int:diagnostic_id>', protocole_views.protocole_create, name='protocole_create'),
    path('protocoles/<int:pk>/', protocole_views.protocole_detail, name='protocole_detail'),
    path('protocoles/<int:pk>/modifier/', protocole_views.protocole_update, name='protocole_update'),
    path('protocoles/<int:pk>/supprimer/', protocole_views.protocole_delete, name='protocole_delete'),
    path('protocoles/<int:pk>/supprimer-fichier/', protocole_views.protocole_delete_file, name='protocole_delete_file'),
    path('protocoles/<int:pk>/modifier-fichier/', protocole_views.protocole_update_file, name='protocole_update_file'),


    path('chat/', chat_views.chat_view, name='chat'),
    path('chat/<str:username>/', chat_views.chat_view, name='chat'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)