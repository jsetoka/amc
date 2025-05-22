from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('accounts/signup/', views.inscription, name='signup'),
    path('accounts/login/', views.connexion, name='login'),
    path('accounts/logout/', views.deconnexion, name='logout'),
    path('accounts/profile/', views.profile, name='profile'),

    path('mot-de-passe-oublie/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('mot-de-passe-envoye/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reinitialiser/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reinitialisation-terminee/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),


    path('vehicules/', views.vehicle_list, name='vehicle_list'),
    path('vehicules/ajouter/', views.vehicle_create, name='vehicle_create'),
    path('vehicules/<int:pk>/', views.vehicle_detail, name='vehicle_detail'),
    path('vehicules/<int:pk>/modifier/', views.vehicle_update, name='vehicle_update'),
    path('vehicules/<int:pk>/supprimer/', views.vehicle_delete, name='vehicle_delete'),

    path('abonnements/', views.abonnement_list, name='abonnement_list'),
    path('vehicules/<int:vehicule_id>/abonnements/', views.abonnement_list_par_vehicule, name='abonnement_list_par_vehicule'),
    path('abonnements/ajouter/', views.abonnement_create, name='abonnement_create'),
    path('abonnements/<int:pk>/', views.abonnement_detail, name='abonnement_detail'),
    path('abonnements/<int:pk>/modifier/', views.abonnement_update, name='abonnement_update'),
    path('abonnements/<int:pk>/supprimer/', views.abonnement_delete, name='abonnement_delete'),

    #path('paiements/', views.paiement_list, name='paiement_list'),
    path('abonnements/<int:abonnement_id>/paiements/', views.paiement_list_par_abonnement, name='paiement_list_par_abonnement'),
    path('paiements/ajouter/<int:abonnement_id>', views.paiement_create, name='paiement_create'),
    path('paiements/<int:pk>/', views.paiement_detail, name='paiement_detail'),
    path('paiements/<int:pk>/modifier/', views.paiement_update, name='paiement_update'),
    path('paiements/<int:pk>/supprimer/', views.paiement_delete, name='paiement_delete'),


    #path('diagnostics/', views.diagnostic_list, name='diagnostic_list'),
    path('vehicules/<int:vehicule_id>/diagnostics/', views.diagnostic_list_par_vehicule, name='diagnostic_list_par_vehicule'),
    path('diagnostics/ajouter/<int:vehicule_id>', views.diagnostic_create, name='diagnostic_create'),
    path('diagnostics/<int:pk>/', views.diagnostic_detail, name='diagnostic_detail'),
    path('diagnostics/<int:pk>/modifier/', views.diagnostic_update, name='diagnostic_update'),
    path('diagnostics/<int:pk>/supprimer/', views.diagnostic_delete, name='diagnostic_delete'),
    path('diagnostics/<int:pk>/supprimer-fichier/', views.diagnostic_delete_file, name='diagnostic_delete_file'),
    path('diagnostics/<int:pk>/modifier-fichier/', views.diagnostic_update_file, name='diagnostic_update_file'),

    #path('protocoles/', views.protocole_list, name='protocole_list'),
    path('diagnostics/<int:diagnostic_id>/protocoles/', views.protocole_list_par_diagnostic, name='protocole_list_par_diagnostic'),
    path('protocoles/ajouter/<int:diagnostic_id>', views.protocole_create, name='protocole_create'),
    path('protocoles/<int:pk>/', views.protocole_detail, name='protocole_detail'),
    path('protocoles/<int:pk>/modifier/', views.protocole_update, name='protocole_update'),
    path('protocoles/<int:pk>/supprimer/', views.protocole_delete, name='protocole_delete'),
    path('protocoles/<int:pk>/supprimer-fichier/', views.protocole_delete_file, name='protocole_delete_file'),
    path('protocoles/<int:pk>/modifier-fichier/', views.protocole_update_file, name='protocole_update_file'),


    path('momopay/', views.momopay, name='momopay'),
    path('momopay/creer_utilisateur/', views.creer_utilisateur, name='creer_utilisateur'),
    # path('momopay/create-momo-user/', views.create_momo_user, name='create_momo_user'),
    path('momopay/requesttopay/', views.requesttopay, name='requesttopay'),
    path('momopay/paymentstatus/', views.paymentstatus, name='paymentstatus'),
    path('momopay/<str:mp>/', views.momopay, name='momopay'),
    path('api/verifier_paiement/<int:abonnement_id>/', views.verifier_paiement, name='verifier_paiement'),
    path('paiement_en_cours/<int:abonnement_id>/', views.paiement_en_cours, name='paiement_en_cours'),

]