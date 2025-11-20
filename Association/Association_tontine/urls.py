from django import views
from django.urls import path,include
from . views import *
from django.contrib import admin
from Association_tontine.views import (
    page_accueil, base, register, 
    landing_page_view,
    tableau_de_bord, tableau_de_bord_global
)
from django.urls import path
from pathlib import Path
#BASE_DIR= Path(_file_).resolve().parent.parent
#from .views import deconnexion



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page_view, name='landing_page'),
    path('connexion/', page_accueil, name='login'),
    path('base/', base, name='base'),
    # ... (the rest of your urlpatterns stay the same)
    path('register/<str:username>/', register, name='register'),
    # les utilisateurs

    path('super-utilisateurs/', liste_super_utilisateurs, name='liste_super_utilisateurs'),
    path('notification/super-utilisateur/<int:user_id>/', notification_super_utilisateur, name='notification_super_utilisateur'),
    path('notification/utilisateur/<int:user_id>/', notification_utilisateur, name='notification_utilisateur'),
    path('notification/super-utilisateur/<int:user_id>/', notification_super_utilisateur, name='notification_super_utilisateur'),
    path('choix-tontine/<int:user_id>/', choix_tontine, name='choix_tontine'),

    # Gestion des membres
    path('membres/', membres, name='membres'),
    path('membres/ajouter/', ajouter_membre, name='ajouter_membre'),
    path('membres/<int:idMembre>/modifier/', modifier_membre, name='modifier_membre'),
    path('membres/<int:idMembre>/supprimer/', supprimer_membre, name='supprimer_membre'),
    path('membres/<int:idMembre>/prets_avaliste/', afficher_prets, name='afficher_prets'),

    # les choix
    #path('page/', page, name='page'),
    path('soumettre_demande/', soumettre_demande, name='soumettre_demande'),
    path('voir_notifications/<int:notification_id>/traiter/', traiter_notification, name='traiter_notification'),
    path('notification_succes/', notification_succes, name='notification_succes'),
    path('confirmation_demande/', confirmation_demande, name='confirmation_demande'),
    path('notifications/', afficher_notifications, name='notifications'),
    path('notification/<int:notification_id>/valider/', valider_demande, name='valider_demande'),
    path('notification/<int:notification_id>/Supprimer/', supprimer_notification, name='supprimer_notification'),
    path('demande/<int:notification_id>/Refuser/',refuser_demande, name='refuser_demande'),
    path('gerer_notifications/', gerer_notifications, name='gerer_notifications'),
    path('modifier_informations/', modifier_informations, name='modifier_informations'),
    path('success_page/', success_page, name='success_page'),
    path('modifier_personnelles/', modifier_personnelles, name='modifier_personnelles'),
    path('choix_tontine/<int:user_id>/', choix_tontine, name='choix_tontine'),
    path('voir_notifications/', voir_notifications, name='voir_notifications'),
    path('notification_super_utilisateur/<int:user_id>/', notification_super_utilisateur, name='notification_super_utilisateur'),
    path('choix_parametres_tontine/<int:user_id>/', choix_parametres_tontine, name='choix_parametres_tontine'),
    
 
    # Gestion des tontines
    path('tontine/', tontine, name='tontine'),
    path('tontine/ajouter/', ajouter_tontine, name='ajouter_tontine'),
    path('tontine/<int:idTontines>/modifier/', modifier_tontine, name='modifier_tontine'),
    path('tontine/<int:idTontines>/supprimer/', supprimer_tontine, name='supprimer_tontine'),

    # Gestion des prêts
    path('prets/', prets, name='prets'),
    path('prets/ajouter/', ajouter_pret, name='ajouter_pret'),
    path('prets/<int:idpret>/modifier/', modifier_pret, name='modifier_pret'),
    path('prets/<int:idpret>/supprimer/', supprimer_pret, name='supprimer_pret'),

    # Gestion des remboursements
    path('remboursements/', remboursements, name='remboursements'),
    path('remboursements/ajouter/', ajouter_remboursement, name='ajouter_remboursement'),
    path('remboursements/<int:idRembo>/modifier/', modifier_remboursement, name='modifier_remboursement'),
    path('remboursements/<int:idRembo>/supprimer/', supprimer_remboursement, name='supprimer_remboursement'),

    # Gestion des dons
    path('dons/', dons, name='dons'),
    path('dons/ajouter/', ajouter_don, name='ajouter_don'),
    path('dons/<int:iddon>/modifier/', modifier_don, name='modifier_don'),
    path('dons/<int:iddon>/supprimer/', supprimer_don, name='supprimer_don'),

    # Gestion des sanctions
    path('sanctions/', sanctions, name='sanctions'),
    path('sanctions/ajouter/', ajouter_sanction, name='ajouter_sanction'),
    path('sanctions/<int:idSanction>/modifier/', modifier_sanction, name='modifier_sanction'),
    path('sanctions/<int:idSanction>/supprimer/', supprimer_sanction, name='supprimer_sanction'),

    # Gestion des épargnes
    path('epargnes/', epargnes, name='epargnes'),
    path('epargnes/ajouter/', ajouter_epargne, name='ajouter_epargne'),
    path('epargnes/<int:idEpargne>/modifier/', modifier_epargne, name='modifier_epargne'),
    path('epargnes/<int:idEpargne>/supprimer/', supprimer_epargne, name='supprimer_epargne'),

    # Gestion des cotisations
    path('cotisations/', cotisations, name='cotisations'),
    path('cotisations/ajouter/', ajouter_cotisation, name='ajouter_cotisation'),
    path('cotisations/<int:codeCotisation>/modifier/', modifier_cotisation, name='modifier_cotisation'),
    path('cotisations/<int:codeCotisation>/supprimer/', supprimer_cotisation, name='supprimer_cotisation'),

    # Gestion des versements
    path('versementsols/', versementsols, name='versementsols'),
    path('versementsols/ajouter/', ajouter_versementsol, name='ajouter_versementsol'),
    path('versementsols/<int:idVersSol>/modifier/', modifier_versementsol, name='modifier_versementsol'),
    path('versementsols/<int:idVersSol>/supprimer/', supprimer_versementsol, name='supprimer_versementsol'),

    path('versementcotisa/', versementcotisa, name='versementcotisa'),
    path('versementcotisa/ajouter/', ajouter_versementcotisa, name='ajouter_versementcotisa'),
    path('versementcotisa/<int:idVersCotis>/modifier/', modifier_versementcotis, name='modifier_versementcotis'),
    path('versementcotisa/<int:idVersCotis>/supprimer/', supprimer_versementcotis, name='supprimer_versementcotis'),

    # Gestion des aides
    path('aides/', aides, name='aides'),
    path('aides/ajouter/', ajouter_aide, name='ajouter_aide'),
    path('aides/<int:numAide>/modifier/', modifier_aide, name='modifier_aide'),
    path('aides/<int:numAide>/supprimer/', supprimer_aide, name='supprimer_aide'),

    # Tableau de bord
    #path('tableau_de_bord/', membre_tableau_de_bord, name='tableau_de_bord'),
    path('tableau_de_bord_global/', tableau_de_bord_global, name='tableau_de_bord_global'),
    # pour mes tests 
    path('membres/<int:idMembre>/tableau_de_bord/', tableau_de_bord, name='membre_tableau_de_bord'),
    path('select-tontine/', select_tontine_view, name='select_tontine'), 
    #path('test_login/', test_login, name='test_login'),
    path('tableau_de_bord/', tableau_de_bord, name='tableau_de_bord'),
    

]



