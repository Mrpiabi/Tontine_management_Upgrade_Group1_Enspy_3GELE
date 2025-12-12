from django.shortcuts import render, redirect
#from django.contrib.auth import login
from django.db.models import Sum, Count,F
from django.db.models.functions import ExtractYear
import pandas as pd
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db import models
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.shortcuts import redirect,get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from .models import membre,don,tontines,Notification,DemandeModification,TontinesMembres, pret, aide,cotisation,versementsol,versementcotis,epargne,remboursement,sanction
from .forms import MembreForm,LoginForm,TontinesForm,UserForm,PretForm,DonForm,AideForm,SanctionForm,RemboursementForm,VersementsolForm,VersementcotisForm,EpargneForm,CotisationForm
from django.db import transaction
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
import string
import random
from django.conf import settings # Import settings
import matplotlib.pyplot as plt
import seaborn as sns
import os # Import os to handle file paths
from datetime import datetime
import json
# Import our NEW form
from .forms import SuperuserCreateMembreForm 
# Create your views here.

def page_accueil(request):
    # Initialize form_data to handle GET requests
    form_data = {}

    # --- SIMPLIFIED AND ROBUST LOGIN LOGIC ---
    if request.method == 'POST':
        username_from_form = request.POST.get('username')
        password_from_form = request.POST.get('password')
        
        # Store the submitted username to re-populate the form if login fails
        form_data['username'] = username_from_form

        # Use Django's built-in authenticate function. It handles everything.
        # It checks if the user exists AND if the password is correct.
        user = authenticate(request, username=username_from_form, password=password_from_form)
        
        if user is not None:
            # A user was successfully authenticated.
            auth_login(request, user)
            
            # Redirect based on user type
            if user.is_superuser:
                return redirect('tableau_de_bord_global')
            else:
                return redirect('tableau_de_bord')
        else:
            # authenticate() returned None. This means the credentials are invalid.
            # We don't know if it's the username or password, which is more secure.
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect. Veuillez réessayer.")

    # --- CHART LOGIC (runs on GET requests and failed logins) ---
    membres = membre.objects.exclude(anneeNais__isnull=True)
    current_year = datetime.now().year
    ages = [current_year - m.anneeNais for m in membres if m.anneeNais and m.anneeNais > 1900]
    
    groupes = {}
    for age in ages:
        tranche = f"{(age//10)*10}-{(age//10)*10+9}"
        groupes[tranche] = groupes.get(tranche, 0) + 1

    context = {
        "groupes_ages_labels": json.dumps(list(groupes.keys())),
        "groupes_ages_values": json.dumps(list(groupes.values())),
        "form_data": form_data, # Pass form_data to the template
    }
    
    return render(request, "accueil.html", context)
#def deconnexion(request):
 #   logout(request)
  #  messages.success(request, 'Vous avez été déconnecté avec succès.')
   # return redirect('login')  # Redirige vers la page de connexion



#from django.core.mail import EmailMultiAlternatives
#from django.template.loader import render_to_string


#def envoyer_recu(membre):
#    sujet = "Confirmation de votre inscription"
#    message = f"""
#Bonjour {membre.nom},

#Merci pour votre inscription à la plateforme Tontine.

#Voici vos informations :
#- Nom : {membre.nom}
#- Email : {membre.email}

#Cordialement,
#Le Groupe 1,
#    """
#    send_mail(sujet, message, 'tonemail@example.com', [membre.email])



def home(request):
    return render(request,'home.html')
def base(request):
     return render(request,'base.html')
  # Assurez-vous d'avoir un formulaire de connexion
from .forms import CustomAuthenticationForm


from django.views.decorators.csrf import csrf_exempt

#@csrf_exempt
#def login(request):
    #if request.method == 'POST':
    #    form = CustomAuthenticationForm(data=request.POST)  # Correction ici
        
        #if form.is_valid():
         #   login_name = form.cleaned_data.get('login').strip()  # Enlever les espaces
         #   password = form.cleaned_data.get('password').strip()  # Enlever les espaces

            # Authentification
          #  try:
                #user = membre.objects.get(login=login_name)
                #membres = membre.objects.get(login=login_name)

        #        if check_password(password, user.password):  # Vérification du mot de passe
         #           request.session['user_id']=user.idMembre
          #          request.session['is_admin']=user.is_admin
           #         user.last_login = timezone.now()
            #        user.save()
              #      next_url = request.POST.get('next') or '/tableau_de_bord/'
                    
                    #if next_url:
             #       return redirect(next_url)

                    # Redirection selon le statut d'administrateur
                    #elif user.is_admin:
                        #return redirect('/tableau_de_bord_global/')  # Admin
                    #else:
                        #return redirect('/tableau_de_bord/')  # Utilisateur
               # else:
                #    messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
            #except membre.DoesNotExist:
             #   messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    #else:
     #   form = CustomAuthenticationForm()  # Formulaire vide pour GET

    #return render(request, 'login.html', {'form': form})

 # Assurez-vous de remplacer par le bon chemin d'importation

  # Renommez l'import

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)

            if user.has_usable_password():
                user_auth = authenticate(request, username=username, password=password)
                #messages.info(request, "Vous devez définir un mot de passe.")
                #return redirect('register', username=username)
                if user_auth is not None:
                    auth_login(request, user_auth)
                    if user_auth.is_superuser:
                        return redirect('tableau_de_bord_global')
                    else:
                        return redirect('page_accueil')
                else:
                    messages.error(request, "Mot de passe incorrect.")
                    return render(request, 'login.html')
            else:
                return redirect('register',username=username)
            
        
        except User.DoesNotExist:
            messages.error(request, "Nom d'utilisateur invalide.")
            return render(request,'login.html')
    return render(request,'login.html')


#import random
#import string

#def generate_password(length=8):
    #Générer un mot de passe aléatoire de 8 caractères
#    characters = string.ascii_letters + string.digits
#    return ''.join(random.choices(characters, k=8))

#from Association_tontine.models import membre
#def ajouter_membre(request):
   # membres = membre.objects.all()
    
    #for m in membres:
       # if not m.user:  # S'il n'a pas encore d'utilisateur lié
            # verifier s'il existe deja un user avec ce login 
            #existing_user = User.objects.filter(username=m.login).first()
            #if existing_user :
            #    m.user = existing_user
            #    m.save()

            # Stocke ou affiche le mot de passe pour donner au membre
            #    print(f"Utilisateur: {m.login} deja existant, associé au membre.") 
            #else:
                # Générer un mot de passe
          #  password = generate_password()
            
            # Créer un nouvel utilisateur
            #user = User.objects.create_user(
            #    username=m.login,   # Le champ login de ton membre
           #     email=m.email,# utiliser email s'il existe sinon vide 
          #      password=password
         #   )
            
            # Lier cet utilisateur au membre
        #    m.user = user
       #     m.save()

      #      # Stocke ou affiche le mot de passe pour donner au membre
     #       print(f"Nouveau utilisateur: {m.login}, crée avec mot de passe: {password}")
    #    else:
    #        print(f"Utilisateur: {m.login}, a deja ete lie ")



#def test_login(request):
#    login_name = 'Dupont'  # Remplacez par le nom d'utilisateur que vous testez
#    password = '1234D'     # Remplacez par le mot de passe d'origine

#    try:
#        user = membre.objects.get(login=login_name)  # Récupération de l'utilisateur
#        if user and user.password:  # Vérifiez que l'utilisateur existe et que le mot de passe n'est pas None
#            # Vérifiez le mot de passe haché
#            if check_password(password, user.password):
#                auth_login(request, user)  # Connecte l'utilisateur
#                user.last_login = timezone.now()  # Met à jour le champ last_login
#                return HttpResponse("Connexion réussie")
#           else:
#                return HttpResponse("Échec de la connexion : mot de passe incorrect")
#        else:
#            return HttpResponse("Échec de la connexion : utilisateur non trouvé")
#    except membre.DoesNotExist:
#        return HttpResponse("Échec de la connexion : utilisateur non trouvé")

from .forms import PasswordRegistrationForm

def register(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request, "Utilisateur introuvable.")
        return redirect('login')
    
    if request.method == 'POST':
        form = PasswordRegistrationForm(request.POST)
        if form.is_valid():

            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            messages.success(request, "Mot de passe défini avec succès. Vous pouvez maintenant vous connecter.")
            return redirect('login')
    else:
       form = PasswordRegistrationForm()

    return render(request, 'register.html', {'form': form, 'username': username})



def liste_super_utilisateurs(request):
    super_utilisateurs = User.objects.filter(is_superuser=True)
    return render(request, 'liste_super_utilisateurs.html', {'super_utilisateurs': super_utilisateurs})

def success_page(request):
    return render(request, 'success_page.html')




def notification_super_utilisateur(request, user_id):
    super_utilisateur = get_object_or_404(User, id=user_id)

    if not super_utilisateur.is_superuser:
        messages.error(request, "Cet utilisateur n'est pas un super utilisateur.")
        return redirect('liste_super_utilisateurs')  # Rediriger vers la liste

    if request.method == 'POST':
        message = request.POST.get('message')
        # Enregistrer la notification
        Notification.objects.create(super_utilisateur=super_utilisateur, message=message)

        messages.success(request, "Notification envoyée au super utilisateur.")
        return redirect('liste_super_utilisateurs')  # Rediriger vers la liste des super utilisateurs

    return render(request, 'notification_super_utilisateur.html', {'super_utilisateur': super_utilisateur})


def gerer_notifications(request):
    if not request.user.is_superuser:
        return redirect('home')  # Redirigez les utilisateurs non autorisés

    notifications = Notification.objects.filter(statut='en_attente')

    if request.method == 'POST':
        id = request.POST.get('id')
        action = request.POST.get('action')

        notification = Notification.objects.get(id=id)
        if action == 'valider':
            notification.statut = 'valide'
            # Traitez la modification ici (mettez à jour les informations de l'utilisateur)
        elif action == 'refuser':
            notification.statut = 'refuse'
        notification.save()

    return render(request, 'gerer_notifications.html', {'notifications': notifications})



from django.core.mail import send_mail
from django.conf import settings
def notification_utilisateur(message, user=None):
    sujet = "Notification Importante"
    corps = message

    if user:
        corps += f"\n\nUtilisateur: {user.username} ({user.email})"

    # Récupérer tous les super utilisateurs
    super_utilisateurs = User.objects.filter(is_superuser=True)

    emails = [admin.email for admin in super_utilisateurs if admin.email]  # Filtrer ceux qui ont une adresse e-mail

    if emails:  # Vérifier si la liste n'est pas vide
        send_mail(
            sujet,
            corps,
            settings.DEFAULT_FROM_EMAIL,
            emails,
            fail_silently=False,
        )




#def choix_tontine(request, user_id):
 #   user = get_object_or_404(membre, user_id=user_id)

 #   if request.method == 'POST':
#        form = TontinesForm(request.POST)  # Crée une instance du formulaire avec les données POST
  #      if form.is_valid():
#            tontine_choisie = form.cleaned_data['tontine']  # Récupère la tontine choisie
#            tontine_choisie.membres.add(user)  # Ajoute le membre à la tontine
#            tontine_choisie.save()

#            Notification.objects.create(
#                utilisateur=membre.user,
#                message=f"{user.nom} a choisi la tontine {tontine_choisie.type_tontine}."
#            )

 #           messages.success(request, "Votre choix de tontine a été enregistré.")

            # Redirection en fonction du nombre de tontines
#            if user.tontines.count() > 2:
#                return redirect('choix_parametres_tontine', user_id=user.id)

#            return redirect('tableau_de_bord')  # Rediriger vers le tableau de bord
 #   else:
 #       form = TontinesForm()  # Crée une instance vide du formulaire

 #   return render(request, 'choix_tontine.html', {'user': user, 'form': form})


from .forms import TontineChoiceForm

def choix_tontine(request):
    if request.method == 'POST':
        form = TontineChoiceForm(request.POST)
        if form.is_valid():
           # Crée une notification pour le super utilisateur
            #super_user = User.objects.get(is_superuser=True)  # Récupère le super utilisateur
            notification = Notification()
            notification.utilisateur = request.user  # Associe la notification au super utilisateur
            notification.details =f"Choix de la tontine : {form.cleaned_data['tontine']}"  # Remplacez par le champ réel
            notification.statut = 'en_attente'
            notification.save()  # Enregistre la notification
            messages.success(request, "Votre choix de tontine a été soumis.")
            return redirect('voir_notifications')  # Redirige vers la page des notifications
    else:
        form = TontineChoiceForm()
    return render(request, 'choix_tontine.html', {'form': form}) 




from .forms import NotificationForm

def soumettre_demande(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification = form.save(commit=False)
            notification.utilisateur = request.user  # Associe la notification à l'utilisateur connecté
            notification.save()
            messages.success(request, "Votre demande de tontine a été soumise avec succès.")
            return redirect('voir_notifications')  # Redirige vers la page des notifications
    else:
        form = NotificationForm()
    return render(request, 'soumettre_demande.html', {'form': form})

def afficher_notifications(request):
    if not request.user.is_superuser:
        return redirect('home')
    #notifications = Notification.objects.filter(utilisateur=request.user)  # Récupère les notifications de l'utilisateur
    notifications = Notification.objects.filter(statut='en_attente')
    return render(request, 'voir_notifications.html', {'notifications': notifications})

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Notification


import logging

# Configurez le logging (ajoutez ceci au début de votre fichier de vues)
logging.basicConfig(level=logging.INFO)

def appliquer_modification(notification):
    try:
        data = json.loads(notification.details)
        logging.info(f"Données extraites : {data}")
    except json.JSONDecodeError:
        logging.error("Erreur de décodage JSON.")
        return False

    type_modif = notification.type_modification
    logging.info(f"Type de modification : {type_modif}")

    if type_modif == 'Tontine':
        try:
            tontine, created = tontines.objects.update_or_create(
                idTontines=data['id'],
                defaults={'nomTontines': data['nom']}
            )
            action = 'créée' if created else 'mise à jour'
            logging.info(f"Tontine {action} : {tontine.nomTontines}")
        except Exception as e:
            logging.error(f"Erreur lors de la mise à jour de la tontine : {e}")
            return False
     #return True  # Indique que la modification a été appliquée avec succès    

            #defaults={'autres_champs': data.get('autres_champs', '')}  # Ajoutez d'autres champs si nécessaire
        #)
        #tontine.nomTontines = data.get('nomTontines')
        #tontine.save()

    elif type_modif == 'Pret':
        prets = pret.objects.get(idMembre_preteur=data['idMembre_preteur'], idMembre_avaliste=data['idMembre_avaliste'])
        prets.montant = data.get('montant')
        prets.pourcentage = data.get('pourcentage')
        prets.date_demande = data.get('date_demande')
        prets.save()

    elif type_modif == 'Remboursement':
        remboursements = remboursement.objects.get(idpret=data['idpret'])
        remboursements.montant_rembourse = data.get('montant_rembourse')
        remboursements.date_remboursement = data.get('date_remboursement')
        remboursements.save()

    elif type_modif == 'Epargne':
        epargnes = epargne.objects.get(idMembre=data['idMembre'], idSeance=data['idSeance'])
        epargnes.montant = data.get('montant')
        epargnes.modeVersement = data.get('modeVersement')
        epargnes.couponVersement = data.get('couponVersement')
        epargnes.save()

   



import json

def valider_demande(request, notification_id):
    # Récupérer la notification
    notification = get_object_or_404(Notification, id=notification_id)

    if request.method == 'POST':
        try:

            details = json.loads(notification.details)
            #id_modification = details.get('id')  # utile pour certains cas
        except json.JSONDecodeError:
            messages.error(request, "Erreur lors de la lecture des détails de la notification.")
            return redirect('voir_notifications')

        # Identifier le membre concerné
        try:
            membre_instance = membre.objects.get(user=notification.utilisateur)
        except membre.DoesNotExist:
            messages.error(request, "Membre lié à l'utilisateur non trouvé.")
            return redirect('voir_notifications')

        # Cas : assigner membre à une tontine
        if notification.type_modification == 'Tontine':
            id_tontine = details.get('id')  # 'id' vient de demande_data['id']
            try:
                tontine_instance = tontines.objects.get(idTontines=id_tontine)
            except tontines.DoesNotExist:
                messages.error(request, "La tontine spécifiée est introuvable.")
                return redirect('voir_notifications')
            
            dernier_numero = TontinesMembres.objects.filter(
                membres=membre_instance, tontines=tontine_instance
                    ).aggregate(models.Max('numero_adhesion'))['numero_adhesion__max'] or 0

            TontinesMembres.objects.create(
                membres=membre_instance,
                tontines=tontine_instance,
                numero_adhesion=dernier_numero + 1
            )

            messages.success(request, f"{membre_instance.nom} a bien été ajouté à la tontine {tontine_instance.nomTontines} avec l'identifiant d'adhésion #{dernier_numero + 1}.")


            # Vérifier s'il est déjà membre de cette tontine
            if TontinesMembres.objects.filter(membres=membre_instance, tontines=tontine_instance).exists():
                messages.warning(request, "Ce membre est déjà inscrit à cette tontine.")
            else:
                # Ajouter l'association
                TontinesMembres.objects.create(membres=membre_instance, tontines=tontine_instance)
                messages.success(request, f"{membre_instance.nom} a bien été ajouté à la tontine {tontine_instance.nomTontines}.")

        elif notification.type_modification == 'Pret':
            id_pret = details.get('idPret')  # Assurez-vous que l'ID du prêt est passé
            pret_instance = get_object_or_404(pret, idpret=id_pret)

            # Récupérer les autres champs nécessaires
            id_membre_avaliste = details.get('idMembre_avaliste')  # ID du membre avaliste
            montant = details.get('montant')
            pourcentage = details.get('pourcentage')
            date_demande = details.get('date_demande')

            # Mise à jour ou création de l'objet Pret
            pret.objects.update_or_create(
                id=pret_instance.idpret,
                defaults={
                    'idMembre_preteur': membre_instance,
                    'idMembre_avaliste': get_object_or_404(membre, idMembre=id_membre_avaliste) if id_membre_avaliste else None,
                    'montant': montant,
                    'pourcentage': pourcentage,
                    'date_demande': date_demande,
                }
            )

        elif notification.type_modification == 'Remboursement':
            remboursement.objects.update_or_create(
                idpret=details.get('idpret'),
                defaults={
                    'montant_rembourse': details.get('montant_rembourse'),
                    'date_remboursement': details.get('date_remboursement'),
                }
            )

        elif notification.type_modification == 'Epargne':
            epargne.objects.update_or_create(
                idMembre=details.get('idMembre'),
                defaults={
                    'montant': details.get('montant'),
                    'modeVersement': details.get('modeVersement'),
                    # Ajoutez d'autres champs nécessaires
                }
            )

        elif notification.type_modification == 'Don':
            don.objects.update_or_create(
                idTontines=details.get('idTontines'),
                defaults={
                    'nature_don': details.get('nature_don'),
                    'montant_don': details.get('montant_don'),
                    'date_don': details.get('date_don'),
                    'description_don': details.get('description_don'),
                }
            )

        elif notification.type_modification == 'Aide':
            aide.objects.update_or_create(
                idMembre=details.get('idMembre'),
                defaults={
                    'date': details.get('date'),
                    'motif_aide': details.get('motif_aide'),
                    'montantAide': details.get('montantAide'),
                    'nomBeneficiaire': details.get('nomBeneficiaire'),
                    # Ajoutez d'autres champs nécessaires
                }
            )

        elif notification.type_modification == 'Sanction':
            sanction.objects.update_or_create(
                idMembre=details.get('idMembre'),
                defaults={
                    'dateSanction': details.get('dateSanction'),
                    'typeSanction': details.get('typeSanction'),
                    'montant': details.get('montant'),
                    'raison': details.get('raison'),
                }
            )

        elif notification.type_modification == 'Versementsol':
            versementsol.objects.update_or_create(
                idMembre=details.get('idMembre'),
                defaults={
                    'montant': details.get('montant'),
                    'modeVersement': details.get('modeVersement'),
                }
            )

        elif notification.type_modification == 'Versementcotis':
            versementcotis.objects.update_or_create(
                idMembre=details.get('idMembre'),
                defaults={
                    'montant': details.get('montant'),
                    'codeCotisation': details.get('codeCotisation'),
                }
            )

        elif notification.type_modification == 'Cotisation':
            cotisation.objects.update_or_create(
                idMembre=details.get('idMembre'),
                defaults={
                    'codeCotisation': details.get('codeCotisation'),
                    'libelle': details.get('libelle'),
                    'nbPartMax': details.get('nbPartMax'),
                }
            )

        # Mettre à jour le statut de la notification
        notification.statut = 'valide'
        notification.save()
        
        messages.success(request, "La demande a été validée et les modifications appliquées avec succès.")
        return redirect('voir_notifications')

    # Affichage de la confirmation si GET
    return render(request, 'confirmation_demande.html', {
        'notification': notification
    })

def refuser_demande(request, notification_id):
    demande = get_object_or_404(Notification, id=notification_id)

    if request.method == 'POST':
        demande.statut = 'refuse'
        demande.save()
        messages.success(request, "La demande a été refusée avec succès.")
        return redirect('tableau_de_bord_global')

    # Si GET, afficher une confirmation simple avant refus
    return render(request, 'refuser_demande.html', {
        'demande': demande,
        'details': demande.details
    })


from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

@login_required
@require_POST
def supprimer_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)

    # Supprimer seulement si traité
    if notification.statut in ['valide', 'refuse']:
        notification.delete()
        messages.success(request, "Notification supprimée avec succès.")
    else:
        messages.warning(request, "Vous ne pouvez supprimer que les notifications traitées.")

    return redirect('voir_notifications')


    # Ici, vous pouvez utiliser notification.type_modification pour déterminer l'action à effectuer
    #notification.statut = 'validée'
   # notification.save()
    #return redirect('notifications')  # Redirige vers la page des notifications

    # Rendre le template avec le contexte de la notification
    #return render(request, 'valider_demandes.html', {'notification': notification})


from django.utils.timezone import make_aware
from datetime import datetime, time

def voir_notifications(request):
    notifications = Notification.objects.all().order_by('-date_envoi')

    return render(request, 'voir_notifications.html', {'notifications': notifications})


#def valider_demande(request, id):
#    notification = get_object_or_404(Notification, id=id)

 #   if request.method == 'POST':
 #       if 'valider' in request.POST:
#            notification.validated = True
 #           notification.save()
 #           messages.success(request, "Demande validée.")
            # Appliquez les modifications ici si nécessaire

 #       elif 'refuser' in request.POST:
  #          messages.error(request, "Demande refusée.")
  #          Notification.objects.create(
  #              utilisateur=notification.utilisateur,
   #             super_utilisateur=notification.utilisateur,
    #            message="Votre demande a été refusée."
     #       )

     #   notification.delete()  # Supprimez la notification après traitement
      #  return redirect('voir_notifications')


#@staff_member_required
def traiter_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, statut='en_attente')

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'valider':
            # Appliquer la modification
            if appliquer_modification(notification):
                notification.statut = 'valide'
                notification.save()
                messages.success(request, "Modification validée et appliquée.")
            else:
                messages.error(request, "Erreur lors de l'application de la modification.")
        elif action == 'refuser':
            notification.statut = 'refuse'
            notification.save()
            messages.info(request, "Modification refusée.")
        else:
            messages.error(request, "Action inconnue.")

        return redirect('voir_notifications')

    return render(request, 'traiter_notification.html', {'notification': notification})





def choix_parametres_tontine(request, user_id):
    user = get_object_or_404(membre, user_id=user_id)
    tontines = user.tontines.all()  # Récupère les tontines de l'utilisateur

    if request.method == 'POST':
        idTontines = request.POST.get('tontine')
        return redirect('page_tontine', idTontines=idTontines)  # Redirige vers la page de la tontine choisie

    return render(request, 'choix_parametres_tontine.html', {'user': user, 'tontines': tontines})


# je vais faire des tests pour voir si le tableau de bord d'un membre est visible 
from django.shortcuts import render, get_object_or_404


def select_tontine_view(request):
    if request.method == 'POST':
        tontine_id = request.POST.get('tontine_id')
        # Logique pour lier le membre à la tontine
        membres = membre.objects.get(login=request.user.login)  # Récupérer le membre connecté
        membres.tontine = tontines.objects.get(id=tontine_id)
        membre.save()
        
        messages.success(request, "Tontine sélectionnée avec succès.")
        return redirect('tableau_de_bord')  # Rediriger vers le tableau de bord du membre
    
    tontine = tontines.objects.all()  # Récupérer toutes les tontines
    return render(request, 'select_tontine.html', {'tontine': tontine})





from django.http import HttpResponseForbidden



#def tableau_de_bord_global(request):
 #   if not request.user.is_superuser:
  #      return HttpResponseForbidden("Vous n'avez pas accès à cette page.")  # Message d'accès interdit

   # membres = membre.objects.all()  # Récupérer tous les membres
    #
    #return render(request, 'tableau_de_bord_global.html', {'membres': membres})


from django.db.models import Sum

# Helper function to check for superuser status
def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser) # Make sure only superusers can see this
def tableau_de_bord_global(request):
    

    # DATA FETCHING & ANALYSIS WITH PANDAS
    # --- Fetch data into Pandas DataFrames ---
    membres_qs = membre.objects.filter(actif=1).values()
    cotisations_qs = cotisation.objects.filter(est_valide=True).values()
    epargnes_qs = epargne.objects.values()
    prets_qs = pret.objects.values('idpret', 'montant', 'pourcentage', 'est_rembourse')
    remboursements_qs = remboursement.objects.values('idpret_id', 'montant_rembourse')

    df_membres = pd.DataFrame(list(membres_qs))
    df_cotisations = pd.DataFrame(list(cotisations_qs))
    df_epargnes = pd.DataFrame(list(epargnes_qs))
    df_prets = pd.DataFrame(list(prets_qs))
    df_remboursements = pd.DataFrame(list(remboursements_qs))

    # --- KPI 1: Total Active Members ---
    total_membres = len(df_membres) if not df_membres.empty else 0

    # --- KPI 2: Total Funds Managed ---
    total_cotise = df_cotisations['montant'].sum() if not df_cotisations.empty else 0
    total_epargne = df_epargnes['montant'].sum() if not df_epargnes.empty else 0
    fonds_totaux = total_cotise + total_epargne

    # --- KPI 3: Total Loans Outstanding ---
    prets_en_cours = 0
    if not df_prets.empty and 'est_rembourse' in df_prets.columns:
        # Filter for active loans
        df_prets_actifs = df_prets[df_prets['est_rembourse'] == False]
        if not df_prets_actifs.empty:
            # Calculate total amount due (principal + interest)
            df_prets_actifs['total_du'] = df_prets_actifs['montant'] * (1 + df_prets_actifs['pourcentage'] / 100)
            
            if not df_remboursements.empty:
                # Calculate total reimbursed for each loan
                df_remb_par_pret = df_remboursements.groupby('idpret_id')['montant_rembourse'].sum().reset_index()
                # Merge the reimbursement data back to the loans dataframe
                df_prets_actifs = pd.merge(df_prets_actifs, df_remb_par_pret, left_on='idpret', right_on='idpret_id', how='left')
                df_prets_actifs['montant_rembourse'] = df_prets_actifs['montant_rembourse'].fillna(0) # Fill NaNs for loans with no reimbursements
            else:
                df_prets_actifs['montant_rembourse'] = 0

            # Calculate remaining amount for each loan and sum it up
            df_prets_actifs['montant_restant'] = df_prets_actifs['total_du'] - df_prets_actifs['montant_rembourse']
            prets_en_cours = df_prets_actifs['montant_restant'].sum()


    # --- Analysis for Charts ---

    # 1. Chart: Member Growth Over Time
    membres_growth_labels = []
    membres_growth_values = []
    if not df_membres.empty and 'anneeEntree' in df_membres.columns:
        df_membres_clean = df_membres.dropna(subset=['anneeEntree']) # Remove rows with no entry year
        membres_par_annee = df_membres_clean.groupby('anneeEntree').size()
        membres_growth_labels = membres_par_annee.index.astype(int).astype(str).tolist()
        membres_growth_values = membres_par_annee.values.tolist()
        
    # 2. Chart: Tontine Popularity
   
    tontines_avec_membres_query = tontines.objects.annotate(num_membres=Count('membres')).order_by('-num_membres')
    tontine_popularity_labels = [t.nomTontines for t in tontines_avec_membres_query]
    tontine_popularity_values = [t.num_membres for t in tontines_avec_membres_query]

    # --- Get the list of members for the table ---
    membres_list = membre.objects.prefetch_related('tontines').filter(actif=1)

    context = {
        'membres': membres_list,
        'kpi': {
            'total_membres': total_membres,
            'fonds_totaux': fonds_totaux,
            'prets_en_cours': prets_en_cours,
        },
        'charts': {
            'membres_growth_labels': membres_growth_labels,
            'membres_growth_values': membres_growth_values,
            'tontine_popularity_labels': tontine_popularity_labels,
            'tontine_popularity_values': tontine_popularity_values,
        }
    }
    
    return render(request, 'tableau_de_bord_global.html', context)

     # Assurez-vous que l'utilisateur est connecté
   
    #membre_utilisateur = get_object_or_404(membre, user=request.user)

    # Récupérer les tontines associées
    #tontine = membre_utilisateur.tontines.all()

    # Récupérer les prêts associés
    #prets = pret.objects.filter(idMembre_preteur=membre_utilisateur,idMembre_avaliste=membre_utilisateur)

    # Récupérer les épargnes associées
    #epargnes = epargne.objects.filter(idMembre=membre_utilisateur)

    # Récupérer les dons associés (ajoutez ce modèle si nécessaire)
    #dons = don.objects.filter(idMembre=membre_utilisateur)

    # Récupérer les cotisations (ajoutez ce modèle si nécessaire)
    #cotisations = cotisation.objects.filter(idMembre=membre_utilisateur)

    # Récupérer les notifications (ajoutez ce modèle si nécessaire)
    #notifications = Notification.objects.filter(utilisateur=membre_utilisateur)

    #return render(request, 'tableau_de_bord_global.html', {
     #   'membre': membre_utilisateur,
    #    'tontine': tontine,
    #    'prets': prets,
    #    'epargnes': epargnes,
    #    'dons': dons,
    #    'cotisations': cotisations,
    #    'notifications': notifications,
    #})

    #if not request.user.is_superuser:
     #   return HttpResponseForbidden("Vous n'avez pas accès à cette page.")

    # Récupérer tous les membres
    #membres = membre.objects.all()  
    # Récupérer d'autres données si nécessaire
    #prets = pret.objects.all()
    #remboursements = remboursement.objects.all()
    #dons = don.objects.all()
    #tontine = tontines.objects.all()

    #context = {
     #   'membres': membres,
      #  'prets': prets,
     #   'remboursements': remboursements,
     #   'dons': dons,
     #   'tontine': tontine,
    #}
    
    #return render(request, 'tableau_de_bord_global.html', context)



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required  # Utilisation du décorateur pour s'assurer que l'utilisateur est connecté
#def tableau_de_bord(request):
    # Récupérer le membre connecté
#    membres = membre.objects.get(login=request.user.username)  # Assurez-vous que 'login' est le bon champ

    # Récupérer les tontines, épargnes, cotisations et remboursements du membre
 #   tontine = tontines.membres.all()  # Récupérer les tontines du membre
  #  epargnes = membres.epargnes.all()  # Récupérer les épargnes
#    cotisations = membres.cotisations.all()  # Récupérer les cotisations
 #   remboursements = membres.remboursements.all()  # Récupérer les remboursements

  #  context = {
#        'membres': membres,  # Notez que j'ai corrigé 'membres' à 'membre' pour être cohérent
 #       'tontine': tontine,
  #      'epargnes': epargnes,
   #     'cotisations': cotisations,
    #    'remboursements': remboursements,
    #}
    #return render(request, 'tableau_de_bord.html', context)



@login_required
def tableau_de_bord(request):
    try:
        # Étape 1 : Récupérer le profil du membre connecté
        membre_info = membre.objects.get(user=request.user)
    except membre.DoesNotExist:
        # Si aucun profil 'membre' n'est associé à l'utilisateur, on affiche une page vide.
        return render(request, 'tableau_de_bord.html', {'membre': None})

    # =================================================================
    # DÉBUT DE L'ANALYSE DE DONNÉES EN PYTHON
    # =================================================================

    # --- KPI 1 : Total Épargné ---
    # Utilise l'ORM Django pour une agrégation SQL efficace
    total_epargne = epargne.objects.filter(idMembre=membre_info).aggregate(total=Sum('montant'))['total'] or 0

    # --- KPI 2 : Dette Actuelle ---
    prets_membre = pret.objects.filter(idMembre_preteur=membre_info, est_rembourse=False)
    dette_actuelle = 0
    for p in prets_membre:
        montant_du = p.montant * (1 + p.pourcentage / 100)
        total_rembourse = remboursement.objects.filter(idpret=p).aggregate(total=Sum('montant_rembourse'))['total'] or 0
        dette_actuelle += (montant_du - total_rembourse)

    # --- KPI 3 : Total Cotisé ---
    total_cotise = cotisation.objects.filter(idMembre=membre_info, est_valide=True).aggregate(total=Sum('montant'))['total'] or 0

    # --- KPI 4 : Nombre de Tontines Actives ---
    tontines_actives = membre_info.tontines.count()


    # --- Analyse pour les Graphiques (avec Pandas) ---

    # 1. Graphique "Répartition des Dépenses" (Pie Chart)
    remboursements_faits = remboursement.objects.filter(idMembre=membre_info).aggregate(total=Sum('montant_rembourse'))['total'] or 0
    
    depenses_data = {
        'Catégorie': ['Cotisations', 'Épargnes', 'Remboursements'],
        'Montant': [total_cotise, total_epargne, remboursements_faits]
    }
    df_depenses = pd.DataFrame(depenses_data)
    # Filtrer les catégories avec un montant nul pour ne pas encombrer le graphique
    df_depenses = df_depenses[df_depenses['Montant'] > 0]


    # 2. Graphique "Historique des Cotisations" (Bar Chart)
    six_months_ago = timezone.now() - timezone.timedelta(days=180)
    cotisations_recentes = cotisation.objects.filter(
        idMembre=membre_info,
        est_valide=True,
        date_paiement__gte=six_months_ago
    ).values('date_paiement', 'montant')

    df_cotis_hist = pd.DataFrame(list(cotisations_recentes))
    cotis_par_mois_labels = []
    cotis_par_mois_values = []
    if not df_cotis_hist.empty:
        df_cotis_hist['date_paiement'] = pd.to_datetime(df_cotis_hist['date_paiement'])
        # Grouper par mois et sommer les montants
        cotis_par_mois = df_cotis_hist.set_index('date_paiement').resample('M')['montant'].sum()
        # Formater pour Chart.js
        cotis_par_mois_labels = cotis_par_mois.index.strftime('%B %Y').tolist()
        cotis_par_mois_values = cotis_par_mois.values.tolist()


    # Préparation du contexte à envoyer au template
    context = {
        'membre': membre_info,
        
        # Les KPIs pour les cartes
        'kpi': {
            'total_epargne': total_epargne,
            'dette_actuelle': dette_actuelle,
            'total_cotise': total_cotise,
            'tontines_actives': tontines_actives,
        },

        # Les données pour les graphiques
        'charts': {
            'depenses_labels': df_depenses['Catégorie'].tolist(),
            'depenses_values': df_depenses['Montant'].tolist(),
            'cotis_hist_labels': cotis_par_mois_labels,
            'cotis_hist_values': cotis_par_mois_values,
        },

        # On garde les listes d'objets si vous voulez toujours les afficher
        'tontines': membre_info.tontines.all(),
        'prets': pret.objects.filter(idMembre_preteur=membre_info),
    }
    
    return render(request, 'tableau_de_bord.html', context)
    #try:
     #   membre_info = membre.objects.get(user=request.user)
        # Récupérer les tontines associées
      #  tontine = membre_info.tontines.all()  # Utilisation de related_name
        # Récupérer les prêts du membre
       # prets_info = pret.objects.filter(idMembre_preteur=membre_info,idMembre_avaliste=membre_info)  
        # Récupérer les épargnes du membre
        #epargnes_info = epargne.objects.filter(idMembre=membre_info)  
    #except membre.DoesNotExist:
     #   membre_info = None
      #  tontine = []
       # prets_info = []
    #    epargnes_info = []
    #except Exception as e:
        # Gérer d'autres exceptions si nécessaire
     #   tontine = []
      #  prets_info = []
       # epargnes_info = []

    #context = {
     #   'membre': membre_info,
      #  'tontine': tontine,
       # 'prets': prets_info,
    #    'epargnes': epargnes_info,
     #   'notifications': request.user.notifications_utilisateur.all(),
    #}
    #return render(request, 'tableau_de_bord.html', context)

@login_required
def membres (request):
    if request.user.is_authenticated:
        # Vérifiez si l'utilisateur est un super utilisateur
        if request.user.is_superuser:
            # Récupérer tous les membres et leurs tontines
            membres = membre.objects.all().prefetch_related('tontines')
        else:
            # Récupérer le membre associé à l'utilisateur connecté
            membre_utilisateur = membre.objects.filter(user=request.user).first()
            if membre_utilisateur:
                # Récupérer toutes les tontines associées à ce membre
                tontines_utilisateur = membre_utilisateur.tontines.all()
                # Récupérer tous les membres associés aux tontines de l'utilisateur
                membres = membre.objects.filter(tontines__in=tontines_utilisateur).distinct()
            else:
                membres = []  # Aucun membre trouvé

        return render(request, 'membre.html', {'membres': membres})
    else:
        return redirect('login')
    #membres = membre.objects.all()  # Récupérer tous les membres
    #return render(request, 'membre.html', {'membres': membres})
    #user = request.user
    #if user.is_superuser:
        # Récupérer les tontines de l'utilisateur
     #   membres=membre.objects.prefetch_related('tontines').all()
      #  tontines = membres.tontines.all()
        


        # Récupérer les membres associés aux tontines de l'utilisateur
       # Membres = membre.objects.filter(tontines__in=tontines).distinct()
        #context = {
         #   'tontines':tontines
            
        #}
        #return render(request, 'membre.html', context)
    #else:
     #   Membres = membre.objects.none()  # Aucun membre si non authentifié
   # context = {
    #  'Membres':Membres
            
    #}
    #return render(request, 'membre.html', context)
        #try:
         #   membre_inst = user.membre
          #  tontines=membre_inst.tontines.all()
        #    membres = membre.objects.filter(tontines__in=tontines).distinct()
        #except membre.DoesNotExist:
         #   membres = membre.objects.none()
    #context = {
     #   'membres':membres
            
    #}
    #return render(request, 'membre.html', context)


        #return render(request, 'membre.html', {'tontine':None})
#from .models import TypeTontine

#from .models import TypeTontine

#def liste_types_tontines(request):
 #   types = TypeTontine.objects.all()
 #   return render(request, 'liste_types_tontines.html', {'types': types})



def tontine(request):
    #type_tontine = get_object_or_404(TypeTontine, id=type_id)
    tontine = tontines.objects.all()
    return render(request, 'tontine.html', { 'tontine': tontine})
    # Récupérer la tontine
    


#from .models import  DemandeParticipation


#@login_required
#def soumettre_demande_participation(request, idTontines):
#    tontine = get_object_or_404(tontines, id=idTontines)
 #   membres = get_object_or_404(membre, user=request.user)

    # Vérifier si une demande existe déjà
 #   if DemandeParticipation.objects.filter(membres=membres, tontine=tontine).exists():
        # Gérer le cas où une demande existe déjà
      #  pass

 #   DemandeParticipation.objects.create(membres=membres, tontine=tontine)
    # Notifier l'administrateur (par exemple, via email ou tableau de bord)
 #   return redirect('tableau_de_bord')


#from django.contrib.admin.views.decorators import staff_member_required

#@staff_member_required
#def gerer_demande_participation(request, demande_id):
#    demande = get_object_or_404(DemandeParticipation, id=demande_id)

 #   if request.method == 'POST':
 #       action = request.POST.get('action')
   #     if action == 'approuver':
 #           demande.approuvee = True
            # Notifier le membre de l'approbation
#        elif action == 'refuser':demande.refusee = True
            # Notifier le membre du refus
 #       demande.save()
  #      return redirect('liste_demandes_participation')
 #   return render(request, 'gerer_demande.html', {'demande': demande})

#from decimal import Decimal
#@login_required
#def soumettre_cotisation(request, idTontines):
#    tontine = get_object_or_404(tontines, id=idTontines)
#    membres = get_object_or_404(membre, user=request.user)

 #   if request.method == 'POST':
 #       montant_type = Decimal(request.POST.get('montant_type'))
  #      if montant_type > tontine.type_tontine.montant:
            # Gérer l'erreur : montant supérieur au montant de la tontine
   #         pass
  #      cotisation.objects.create(membres=membres, tontine=tontine, montant_type=montant_type)
 #       return redirect('tableau_de_bord')
 #   return render(request, 'soumettre_cotisation.html', {'tontine': tontine})



def creer_pret(request):

    if request.method == 'POST':
        form = PretForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('prets')  # Rediriger vers une page de liste des prêts
    else:
        form = PretForm()
    return render(request, 'creer_pret.html', {'form': form})
 


#def prets(request):
    
#    prets = pret.objects.all()  # Récupère tous les prêts
 #   return render(request, 'pret.html', {'prets': prets})
   
    
def prets(request):
    #prets = get_object_or_404(pret, idpret=idpret)
    prets = pret.objects.all()
    
    context = {
        'prets': prets,
        #'remboursements': remboursements,
    }
    return render(request, 'pret.html', context)
   
def epargnes(request):
    # Récupération des membres, par exemple tous les membres ou filtrés
    membres = membre.objects.all()  # Assurez-vous que Membre est bien importé

    # Pour récupérer toutes les épargnes associées aux membres
    epargnes = epargne.objects.filter(idMembre__in=membres)

    # Passer les données au contexte pour le template
    context = {
        'epargnes': epargnes,
        'membres': membres,
    }
    
    return render(request, 'epargne.html', context)
def aides(request):
    
    membres = membre.objects.get(user=request.user)
    aides = aide.objects.all(membres=membres)  # Récupérer tous les membres
    return render(request, 'aide.html', {'aides': aides})
   
    

def versementsols(request):

    membres = membre.objects.get(user=request.user)
    versementsols = versementsol.objects.all(membres=membres)  # Récupérer tous les membres
    return render(request, 'versementsol.html', {'versementsols': versementsols})

  
def versementcotisa(request):
    
    membres = membre.objects.get(user=request.user)
    versementcotisa = versementcotis.objects.all(membres=membres)  # Récupérer tous les membres
    return render(request, 'versementcotis.html', {'versementcotisa': versementcotisa})

  
def cotisations(request):
    
    # Récupération des membres, par exemple tous les membres ou filtrés
    membres = membre.objects.all()  # Assurez-vous que Membre est bien importé

    # Pour récupérer toutes les épargnes associées aux membres
    cotisations = cotisation.objects.filter(idMembre__in=membres)

    # Passer les données au contexte pour le template
    context = {
        'cotisations': cotisations,
        'membres': membres,
    }
    
    return render(request, 'cotisation.html', context)
def sanctions(request):
    
    membres = membre.objects.get(user=request.user)
    sanctions = sanction.objects.all(membres=membres)  # Récupérer tous les membres
    return render(request, 'sanction.html', {'sanctions': sanctions})
   
   
#def remboursements(request):
    
 #   remboursements = remboursement.objects.select_related('idpret__idMembre_preteur', 'idpret__idMembre_avaliste').all()
  #  return render(request, 'remboursement.html', {'remboursements': remboursements})


def remboursements(request):
    # Récupérer le prêt correspondant
    #pret_info = get_object_or_404(pret, idpret=idpret)
    
    # Récupérer les remboursements associés à ce prêt
    remboursements = remboursement.objects.all()

    context = {
        #'pret': pret_info,
        'remboursements': remboursements
    }
    return render(request, 'remboursement.html', context)


def dons(request):
    
    dons = don.objects.all()  # Récupérer tous les membres
    return render(request, 'don.html', {'dons': dons})
   


# Helper function to generate a random password
def generate_random_password(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

# Helper function to check for superuser status
def is_superuser(user):
    return user.is_superuser



@user_passes_test(is_superuser)
def ajouter_membre(request):
    if request.method == 'POST':
        form = SuperuserCreateMembreForm(request.POST) # Utilise le nouveau formulaire
        if form.is_valid():
            data = form.cleaned_data
            email = data['email']
            
            try:
                with transaction.atomic():
                    # 1. Générer un mot de passe temporaire
                    temp_password = generate_random_password()

                    # 2. Créer le compte Utilisateur Django
                    new_user = User.objects.create_user(
                        username=email,
                        email=email,
                        password=temp_password,
                        first_name=data['prenom'],
                        last_name=data['nom']
                    )
                    
                    # 3. Créer le profil 'membre' correspondant et le lier
                    membre.objects.create(
                        user=new_user,
                        nom=data['nom'],
                        prenom=data['prenom'],
                        email=email,
                        login=email,
                        anneeEntree=data['anneeEntree'],
                        sexe=data['sexe'],
                        engagement=data['engagement'],
                        telephone1=data['telephone1'],
                        anneeNais=data.get('anneeNais'),
                        telephone2=data.get('telephone2'),
                        actif=1
                    )
                
                # 4. Afficher les identifiants à l'administrateur
                success_message = (
                    f"Le membre '{data['prenom']} {data['nom']}' a été créé avec succès. "
                    f"Le nouveau compte est : "
                    f"Nom d'utilisateur = {email} | "
                    f"Mot de passe temporaire = {temp_password}"
                )
                messages.success(request, success_message)
                
                #return redirect('membres') # Redirige vers la liste des membres
                form = SuperuserCreateMembreForm()

            except Exception as e:
                messages.error(request, f"Une erreur inattendue est survenue : {e}")

    else: # Requête GET
        form = SuperuserCreateMembreForm()

    return render(request, 'ajouter_membre.html', {'form': form})



def ajouter_tontine(request):
    if request.method == 'POST':
        form = TontinesForm(request.POST)
        if form.is_valid():
            form.save()  # Enregistrer le membre dans la base de données
            return redirect('tontine')  # Rediriger vers la liste des membres
    else:
        form = TontinesForm()
    return render(request, 'ajouter_tontine.html', {'form': form})



def ajouter_pret(request):
    if request.method == 'POST':
        form = PretForm(request.POST)
        if form.is_valid():
            form.save()  # Enregistrer le membre dans la base de données
            return redirect('prets')  # Rediriger vers la liste des membres
    else:
        form = PretForm()
    return render(request, 'ajouter_pret.html', {'form': form})


from django.shortcuts import render, redirect
from .forms import (PretForm, DonForm, AideForm, SanctionForm, RemboursementForm, 
                    VersementsolForm, VersementcotisForm, EpargneForm, CotisationForm, TontineChoiceForm)

def modifier_informations(request):
    if request.method == 'POST':
        # Exemples d'identification du formulaire soumis via le name des boutons submit
        if 'modifier_tontine' in request.POST:
            form = TontineChoiceForm(request.POST)
            if form.is_valid():
                tontine = form.cleaned_data['tontine']  # selon champ du form
                request.session['demande_type'] = 'Tontine'
                request.session['demande_data'] = {
                    'id': tontine.idTontines,
                    'nom': getattr(tontine, 'nomTontines', 'N/A'),
                }
                return redirect('confirmation_demande')

        elif 'modifier_pret' in request.POST:
            form = PretForm(request.POST)
            if form.is_valid():
                # Tu n'as pas de champ "pret" dans le form, donc on récupère les champs pertinents
                data = form.cleaned_data
                request.session['demande_type'] = 'Pret'
                request.session['demande_data'] = {
                    'idMembre_preteur': data.get('idMembre_preteur').idMembre if data.get('idMembre_preteur') else None,
                    'idMembre_avaliste': data.get('idMembre_avaliste').idMembre if data.get('idMembre_avaliste') else None,
                    'montant': str(data.get('montant')),
                    'pourcentage': str(data.get('pourcentage')),
                    'date_demande': str(data.get('date_demande')),
                }
                return redirect('confirmation_demande')

        elif 'modifier_remboursement' in request.POST:
            form = RemboursementForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                request.session['demande_type'] = 'Remboursement'
                request.session['demande_data'] = {
                    'idpret': data.get('idpret').idpret if data.get('idpret') else None,
                    'montant_rembourse': str(data.get('montant_rembourse')),
                    'date_remboursement': str(data.get('date_remboursement')),
                }
                return redirect('confirmation_demande')

        elif 'modifier_epargne' in request.POST:
            form = EpargneForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                request.session['demande_type'] = 'Epargne'
                request.session['demande_data'] = {
                    'montant': str(data.get('montant')),
                    'modeVersement': data.get('modeVersement'),
                    'couponVersement': data.get('couponVersement'),
                    'idMembre': data.get('idMembre').idMembre if data.get('idMembre') else None,
                    'idSeance': data.get('idSeance').idSeance if data.get('idSeance') else None,
                }
                return redirect('confirmation_demande')

        elif 'modifier_don' in request.POST:
            form = DonForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                request.session['demande_type'] = 'Don'
                request.session['demande_data'] = {
                    'nature_don': data.get('nature_don'),
                    'montant_don': str(data.get('montant_don')),
                    'date_don': str(data.get('date_don')),
                    'description_don': data.get('description_don'),
                    'idTontines': data.get('idTontines').idTontines if data.get('idTontines') else None,
                    'idMembre': data.get('idMembre').idTontines if data.get('idMembre') else None,
                }
                return redirect('confirmation_demande')

        elif 'modifier_aide' in request.POST:
            form = AideForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                request.session['demande_type'] = 'Aide'
                request.session['demande_data'] = {
                    'date': str(data.get('date')),
                    'motif_aide': data.get('motif_aide'),
                    'montantAide': str(data.get('montantAide')),
                    'nomBeneficiaire': data.get('nomBeneficiaire'),
                    'lienBeneficiareAvecMembre': data.get('lienBeneficiareAvecMembre'),
                    'type_aide': data.get('type_aide'),
                    'lieu': data.get('lieu'),
                    'idMembre': data.get('idMembre').idMembre if data.get('idMembre') else None,
                }
                return redirect('confirmation_demande')

        elif 'modifier_sanction' in request.POST:
            form = SanctionForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                request.session['demande_type'] = 'Sanction'
                request.session['demande_data'] = {
                    'dateSanction': str(data.get('dateSanction')),
                    'typeSanction': data.get('typeSanction'),
                    'montant': str(data.get('montant')),
                    'raison': data.get('raison'),
                    'idMembre': data.get('idMembre').idMembre if data.get('idMembre') else None,
                }
                return redirect('confirmation_demande')

        elif 'modifier_versementsol' in request.POST:
            form = VersementsolForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                request.session['demande_type'] = 'Versementsol'
                request.session['demande_data'] = {
                    'montant': str(data.get('montant')),
                    'modeVersement': data.get('modeVersement'),
                    'couponVersement': data.get('couponVersement'),
                    'idMembre': data.get('idMembre').idMembre if data.get('idMembre') else None,
                    'idSeance': data.get('idSeance').idSeance if data.get('idSeance') else None,
                }
                return redirect('confirmation_demande')

        elif 'modifier_versementcotis' in request.POST:
            form = VersementcotisForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                request.session['demande_type'] = 'Versementcotis'
                request.session['demande_data'] = {
                    'montant': str(data.get('montant')),
                    'modeVersement': data.get('modeVersement'),
                    'couponVersement': data.get('couponVersement'),
                    'codeCotisation': data.get('codeCotisation'),
                    'idMembre': data.get('idMembre').idMembre if data.get('idMembre') else None,
                    'idSeance': data.get('idSeance').idSeance if data.get('idSeance') else None,
                }
                return redirect('confirmation_demande')

        elif 'modifier_cotisation' in request.POST:
            form = CotisationForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                request.session['demande_type'] = 'Cotisation'
                request.session['demande_data'] = {
                    'codeCotisation': data.get('codeCotisation'),
                    'libelle': data.get('libelle'),
                    'nbPartMax': data.get('nbPartMax'),
                    'montant': str(data.get('montant')),
                    'idMembre': data.get('idMembre').idMembre if data.get('idMembre') else None,
                    'tontine': data.get('tontine').idTontines if data.get('tontine') else None,
                    'penaliteDefaillanceBenef': str(data.get('penaliteDefaillanceBenef')),
                    'penaliteDefaillanceNonBenef': str(data.get('penaliteDefaillanceNonBenef')),
                    'miseAPrix': str(data.get('miseAPrix')),
                }
                return redirect('confirmation_demande')

        else:
            # Formulaire inconnu, on peut afficher une erreur ou rediriger
            return redirect('modifier_informations')

        # Si formulaire invalide, on réaffiche tous les formulaires avec erreurs et données saisies
        forms = {
            'tontine_form': TontineChoiceForm(request.POST),
            'pret_form': PretForm(request.POST),
            'remboursement_form': RemboursementForm(request.POST),
            'epargne_form': EpargneForm(request.POST),
            'don_form': DonForm(request.POST),
            'aide_form': AideForm(request.POST),
            'sanction_form': SanctionForm(request.POST),
            'versementsol_form': VersementsolForm(request.POST),
            'versementcotis_form': VersementcotisForm(request.POST),
            'cotisation_form': CotisationForm(request.POST),
        }
        return render(request, 'modifier_informations.html', {'forms': forms})

    else:
        # Méthode GET, afficher tous les formulaires vides
        forms = {
            'tontine_form': TontineChoiceForm(),
            'pret_form': PretForm(),
            'remboursement_form': RemboursementForm(),
            'epargne_form': EpargneForm(),
            'don_form': DonForm(),
            'aide_form': AideForm(),
            'sanction_form': SanctionForm(),
            'versementsol_form': VersementsolForm(),
            'versementcotis_form': VersementcotisForm(),
            'cotisation_form': CotisationForm(),
        }
        return render(request, 'modifier_informations.html', {'forms': forms})

from django.utils import timezone
import json

def confirmation_demande(request):
    if request.method == 'POST':
        if 'confirmer' in request.POST:
            demande_type = request.session.get('demande_type')
            demande_data = request.session.get('demande_data')

            if demande_type and demande_data:
                details_str = json.dumps(demande_data, indent=2, default=str)

                Notification.objects.create(
                    utilisateur=request.user,
                    type_modification=demande_type,
                    details=details_str,
                    statut='en_attente',
                    date_envoi=timezone.now(),
                )

                request.session.pop('demande_type', None)
                request.session.pop('demande_data', None)

                return redirect('notification_succes')

        elif 'annuler' in request.POST:
            return redirect('modifier_informations')

        # ✅ Ajouter une redirection ou une réponse par défaut ici :
        return redirect('modifier_informations')  # ou autre vue par défaut

    else:
        demande_type = request.session.get('demande_type')
        demande_data = request.session.get('demande_data')
        return render(request, 'confirmation_demande.html', {
            'demande_type': demande_type,
            'demande_data': demande_data,
        })







def notification_succes(request):
    return render(request, 'notification_succes.html')



#def confirmation_demande(request):
#    demande_type = request.session.get('demande_type')
#    demande_data = request.session.get('demande_data')

#    if request.method == 'POST':
#        # Créer une notification
 #       Notification.objects.create(
 #           utilisateur=request.user,
 #           details=f"Demande de modification de {demande_type} : {demande_data}",
      #      statut='en_attente'
 #       )
#        return redirect('voir_notifications')

#    return render(request, 'confirmation_demande.html', {
 #       'demande_type': demande_type,
   #     'demande_data': demande_data
#    })



    #if request.method == 'POST':
     #   type_modification = request.POST.get('type_modification')
    #    details = request.POST.get('details')

        # Créer une nouvelle notification
    #    notification = Notification(utilisateur=request.user, type_modification=type_modification, details=details, statut='en_attente')
     #   notification.save()
     #   return redirect('success_page')  # Redirige vers une page de succès ou de confirmation

   # return render(request, 'modifier_informations.html')
    #if request.method == 'POST':
        # Logique pour récupérer les données du formulaire
        # Exemple : montant, type de prêt, etc.

        # Créer une notification pour le superutilisateur
     #   Notification.objects.create(
      #      membre=request.user,
       #     message="Demande de modification ou d'ajout de données reçue."
        #)

       # messages.success(request, "Votre demande a été envoyée pour approbation.")
        #return redirect('tableau_de_bord')

   # return render(request, 'ajouter_modification.html')
    #if request.method == 'POST':
        # Récupérer le type d'information à modifier
     #   type_modification = request.POST.get('type_modification')

      #  if type_modification:
       #     return redirect(f'modifier_{type_modification}')  # Redirection vers la vue spécifique

   # return render(request, 'modifier_informations.html')

def modifier_personnelles(request):
    if request.method == 'POST':
        # Traiter la demande de modification des informations personnelles
        nouveau_message = request.POST.get('message')
        # Créer une notification pour le superutilisateur
        Notification.objects.create(
            membre=request.user,
            super_utilisateur=...,  # Identifiez le superutilisateur
            message=nouveau_message
        )
        messages.success(request, "Votre demande a été envoyée.")
        return redirect('tableau_de_bord')

    return render(request, 'modifier_personnelles.html')




def ajouter_don(request):
    if request.method == 'POST':
        form = DonForm(request.POST)
        if form.is_valid():
            form.save()  # Enregistrer le membjouter_aide.htmlre dans la base de données
            return redirect('dons')  # Rediriger vers la liste des membres
    else:
        form = DonForm()
    return render(request, 'ajouter_don.html', {'form': form})


def ajouter_sanction(request):
    if request.method == 'POST':
        form = SanctionForm(request.POST)
        if form.is_valid():
            form.save()  # Enregistrer le membre dans la base de données
            return redirect('sanctions')  # Rediriger vers la liste des membres
    else:
        form =SanctionForm()
    return render(request, 'ajouter_sanction.html', {'form': form})



def ajouter_aide(request):
    if request.method == 'POST':
        form = AideForm(request.POST)
        if form.is_valid():
            form.save()  # Enregistrer le membre dans la base de données
            return redirect('aides')  # Rediriger vers la liste des membres
    else:
        form = AideForm()
    return render(request, 'ajouter_aide.html', {'form': form})


#def ajouter_remboursement(request):
#    if request.method == 'POST':
#        form = RemboursementForm(request.POST)
#        if form.is_valid():
#            form.save()  # Enregistrer le membre dans la base de données
#            return redirect('remboursements')  # Rediriger vers la liste des membres
#    else:
 #       form = RemboursementForm()
 #   return render(request, 'ajouter_remboursement.html', {'form': form})

def ajouter_remboursement(request):
    if request.method == 'POST':
        form = RemboursementForm(request.POST)
        if form.is_valid():
            remboursement = form.save(commit=False)
            remboursement.save()  # Enregistrer le remboursement
            return redirect('prets')  # Rediriger vers la liste des prêts
    else:
        form = RemboursementForm()

    prets = pret.objects.all()
    return render(request, 'ajouter_remboursement.html', {'form': form, 'prets': prets})




def ajouter_versementsol(request):
    if request.method == 'POST':
        form = VersementsolForm(request.POST)
        if form.is_valid():
            form.save()  # Enregistrer le membre dans la base de données
            return redirect('versementsols')  # Rediriger vers la liste des membres
    else:
        form = VersementsolForm()
    return render(request, 'ajouter_versementsol.html', {'form': form})


def ajouter_versementcotisa(request):
    if request.method == 'POST':
        form = VersementcotisForm(request.POST)
        if form.is_valid():
            form.save()  # Enregistrer le membre dans la base de données
            return redirect('versementcotisa')  # Rediriger vers la liste des membres
    else:
        form = VersementcotisForm()
    return render(request, 'ajouter_versementcotisa.html', {'form': form})

def ajouter_epargne(request):
    if request.method == 'POST':
        form = EpargneForm(request.POST)
        if form.is_valid():
            form.save()  # Enregistrer le membre dans la base de données
            return redirect('epargnes')  # Rediriger vers la liste des membres
    else:
        form = EpargneForm()
    return render(request, 'ajouter_epargne.html', {'form': form})



def ajouter_cotisation(request):
    if request.method == 'POST':
        form = CotisationForm(request.POST)
        if form.is_valid():
            form.save()  # Enregistrer le membre dans la base de données
            return redirect('cotisations')  # Rediriger vers la liste des membres
    else:
        form = CotisationForm()
    return render(request, 'ajouter_cotisation.html', {'form': form})


#@login_required
#def supprimer_membre(request, idMembre):
 #   membre_instance = get_object_or_404(membre, idMembre=idMembre)
 #   if request.method == 'POST':
 #       user = membre_instance.user
 #       user.delete()
 #       return redirect('membres')
 #   return render(request, 'supprimer_membre.html', {'membre_instance': membre_instance})


def supprimer_membre(request, idMembre):
    membres = get_object_or_404(membre, pk=idMembre)

    if request.method == 'POST':
        # 1) Désactive le membre
        membres.actif = 0
        membres.save()

        cotisation.objects.filter(idMembre=membres).delete()

        # 2) Supprime toutes ses cotisations (via le bon champ FK)
        #    Ici j’imagine que Cotisation.membre pointe vers Membre
        #cotisation.objects.filter(idMembre=membres).delete()

        # 3) Supprime l’utilisateur associé
        if membres.user:
            membres.user.delete()
            

        return redirect('membres')
    return render(request, 'supprimer_membre.html', {'membres': membres})

def supprimer_tontine(request, idTontines):
    tontine = get_object_or_404(tontines, idTontines=idTontines)
    if request.method == "POST":
        tontine.delete()  # Supprime le membre
        messages.success(request, "Tontine supprimée avec succès.")
        return redirect('tontine')
      # Redirige vers la liste des membres
    return render(request, 'supprimer_tontine.html', {'tontine': tontine})  # Utilisez idMembre
      # Redirige vers la liste des membres


def supprimer_aide(request, numAide):
    aides = get_object_or_404(aide, numAide = numAide)
    if request.method == "POST":
        aides.delete()  # Supprime le membre
        messages.success(request, "Tontine supprimée avec succès.")
        return redirect('aides')  # Redirige vers la liste des membres
      # Redirige vers la liste des membres
    return render(request, 'supprimer_aide.html', {'aides': aides})  # Utilisez idMembre
      # Redirige vers la liste des membres  # Utilisez idMembre
    

def supprimer_cotisation(request, codeCotisation ):
    cotisations = get_object_or_404(cotisation, codeCotisation =codeCotisation ) 
    if request.method == "POST":
        cotisations.delete()   # Supprime le membre
        messages.success(request, "Cotisation supprimée avec succès.")
        return redirect('cotisations')  # Redirige vers la liste des membres
      # Redirige vers la liste des membres
    return render(request, 'supprimer_cotisation.html', {'cotisations': cotisations})  # Utilisez idMembre
      # Redirige vers la liste des membres  # Utilisez idMembre
    


def supprimer_epargne(request, idEpargne):
    epargnes = get_object_or_404(epargne, idEpargne=idEpargne)  # Utilisez idMembre
     # Redirige vers la liste des membres
    if request.method == "POST":
        epargnes.delete()  # Supprime le membre
        messages.success(request, "Epargne supprimée avec succès.")
        return redirect('epargnes')  # Redirige vers la liste des membres
      # Redirige vers la liste des membres
    return render(request, 'supprimer_epargne.html', {'epargnes': epargnes})  # Utilisez idMembre
      # Redirige vers la liste des membres  # Utilisez idMembre
    


def supprimer_remboursement(request, idRembo):
    remboursements = get_object_or_404(remboursement, idRembo=idRembo)
    if request.method == "POST":
        remboursements.delete()   # Supprime le membre
        messages.success(request, "Remboursement supprimé avec succès.")
        return redirect('remboursements')  # Redirige vers la liste des membres
      # Redirige vers la liste des membres
    return render(request, 'supprimer_remboursement.html', {'remboursements': remboursements})  # Utilisez idMembre
     

def supprimer_sanction(request, idSanction):
    sanctions = get_object_or_404(sanction, idSanction=idSanction)  # Utilisez idMembre
    if request.method == "POST":
        sanctions.delete()  # Supprime le membre
        messages.success(request, "Sanction supprimée avec succès.")
        return redirect('sanctions')  # Redirige vers la liste des membres
      # Redirige vers la liste des membres
    return render(request, 'supprimer_sanction.html', {'sanctions': sanctions})  # Utilisez idMembre
     
    


def supprimer_versementcotis(request, idVersCotis):
    versementcotisa = get_object_or_404(versementcotis, idVersCotis=idVersCotis)  # Utilisez idMembre
    if request.method == "POST":
        versementcotisa.delete()  # Supprime le membre
        messages.success(request, "Versement de cotisation supprimée avec succès.")
        return redirect('versementcotisa')  # Redirige vers la liste des membres
      # Redirige vers la liste des membres
    return render(request, 'supprimer_versementcotis.html', {'versementcotisa': versementcotisa})  # Utilisez idMembre
     
      


def supprimer_versementsol(request, idVersSol):
    versementsols = get_object_or_404(versementsol, idVersSol=idVersSol)  # Utilisez idMembre
    if request.method == "POST":
        versementsols.delete()   # Supprime le membre
        messages.success(request, "Remboursement supprimé avec succès.")
        return redirect('versementsols')  # Redirige vers la liste des membres
      # Redirige vers la liste des membres
    return render(request, 'supprimer_versementsol.html', {'versementsols': versementsols})  # Utilisez idMembre
     
      # Supprime le membre
      # Redirige vers la liste des membres


def supprimer_don(request, iddon):
    dons = get_object_or_404(don, iddon=iddon)  # Utilisez idMembre
    if request.method == "POST":
        dons.delete()   # Supprime le membre
        messages.success(request, "Don supprimé avec succès.")
        return redirect('dons')  # Redirige vers la liste des membres
      # Redirige vers la liste des membres
    return render(request, 'supprimer_don.html', {'dons': dons})  # Utilisez idMembre
     
     # Supprime le membre
      # Redirige vers la liste des membres

#def page(request):
 #   return render(request,'page.html')       



def supprimer_pret(request, idpret):
    prets = get_object_or_404(pret,idpret=idpret)  # Utilisez idMembre
    if request.method == "POST":
        prets.delete()    # Supprime le membre
        messages.success(request, "Pret supprimé avec succès.")
        return redirect('prets')  # Redirige vers la liste des membres
      # Redirige vers la liste des membres
    return render(request, 'supprimer_pret.html', {'prets': prets})  # Utilisez idMembre
     
   




def modifier_membre(request, idMembre):
    membre_instance = get_object_or_404(membre, idMembre=idMembre)
    if request.method == 'POST':
        form = MembreForm(request.POST, instance=membre_instance)
        if form.is_valid():
            form.save()
            return redirect('membres')
    else:
        form = MembreForm(instance=membre_instance)
    return render(request, 'modifier_membre.html', {'form': form})  # Passer le membre au template


def modifier_tontine(request, idTontines):
    tontine = get_object_or_404(tontines, idTontines=idTontines)
    if request.method == 'POST':
        form = TontinesForm(request.POST, instance=tontine)
        if form.is_valid():
            form.save()
            return redirect('tontine')
    else:
        form = TontinesForm(instance=tontine)
    return render(request, 'modifier_tontine.html', {'form': form})


def modifier_aide(request, numAide):
    aides = get_object_or_404(aide, numAide=numAide)
    if request.method == 'POST':
        form = AideForm(request.POST, instance=aides)
        if form.is_valid():
            form.save()
            return redirect('aides')
    else:
        form = AideForm(instance=aides)
    return render(request, 'modifier_aide.html', {'form': form})


def modifier_sanction(request, idSanction):
    sanctions = get_object_or_404(sanction, idSanction=idSanction)
    if request.method == 'POST':
        form = SanctionForm(request.POST, instance=sanctions)
        if form.is_valid():
            form.save()
            return redirect('sanctions')
    else:
        form = SanctionForm(instance=sanctions)
    return render(request, 'modifier_sanction.html', {'form': form})# une classe est constitue d'un nom et le nom de la class commence toujours par la majuscule ensuite les attributs ou les proprietes de la classe et la methode de la classe 



def modifier_remboursement(request, idRembo):
    remboursements = get_object_or_404(remboursement, idRembo=idRembo)
    if request.method == 'POST':
        form = RemboursementForm(request.POST, instance=remboursements)
        if form.is_valid():
            form.save()
            return redirect('remboursements')
    else:
        form = RemboursementForm(instance=remboursements)
    return render(request, 'modifier_remboursement.html', {'form': form})# une classe est constitue d'un nom et le nom de la class commence toujours par la majuscule ensuite les attributs ou les proprietes de la classe et la methode de la classe 




def modifier_epargne(request, idEpargne):
    epargnes = get_object_or_404(epargne, idEpargne = idEpargne)  # Utilisez idMembre
    if request.method == 'POST':
        form = EpargneForm(request.POST, instance=epargnes)
        if form.is_valid():
            form.save()
            return redirect('epargnes')
    else:
        form = EpargneForm(instance=epargnes)
    return render(request, 'modifier_epargne.html', {'form': form})# une classe est constitue d'un nom et le nom de la class commence toujours par la majuscule ensuite les attributs ou les proprietes de la classe et la methode de la classe 




def modifier_pret(request, idpret):
    prets = get_object_or_404(pret, idpret = idpret)  # Utilisez idMembre
    if request.method == 'POST':
        form = PretForm(request.POST, instance=prets)
        if form.is_valid():
            form.save()
            return redirect('prets')
    else:
        form = PretForm(instance=prets)
    return render(request, 'modifier_pret.html', {'form': form})# une classe est constitue d'un nom et le nom de la class commence toujours par la majuscule ensuite les attributs ou les proprietes de la classe et la methode de la classe 




def modifier_versementcotis(request, idVersCotis):
    versementcotisa = get_object_or_404(versementcotis, idVersCotis = idVersCotis)  # Utilisez idMembre
    if request.method == 'POST':
        form = VersementcotisForm(request.POST, instance=versementcotisa )
        if form.is_valid():
            form.save()
            return redirect('versementcotisa')
    else:
        form = VersementcotisForm(instance=versementcotisa )
    return render(request, 'modifier_versementcotis.html', {'form': form})# une classe est constitue d'un nom et le nom de la class commence toujours par la majuscule ensuite les attributs ou les proprietes de la classe et la methode de la classe 





def modifier_versementsol(request, idVersSol):
    versementsols = get_object_or_404(versementsol, idVersSol = idVersSol)  # Utilisez idMembre
    if request.method == 'POST':
        form =VersementsolForm(request.POST, instance=versementsols)
        if form.is_valid():
            form.save()
            return redirect('versementsols')
    else:
        form = VersementsolForm(instance=versementsols)
    return render(request, 'modifier_versementsol.html', {'form': form})# une classe est constitue d'un nom et le nom de la class commence toujours par la majuscule ensuite les attributs ou les proprietes de la classe et la methode de la classe 



def modifier_cotisation(request, codeCotisation):
    cotisations = get_object_or_404(cotisation, codeCotisation = codeCotisation)  # Utilisez idMembre
    if request.method == 'POST':
        form =CotisationForm(request.POST, instance=cotisations)
        if form.is_valid():
            form.save()
            return redirect('cotisations')
    else:
        form = CotisationForm(instance=cotisations)
    return render(request, 'modifier_cotisation.html', {'form': form})# une classe est constitue d'un nom et le nom de la class commence toujours par la majuscule ensuite les attributs ou les proprietes de la classe et la methode de la classe 



def modifier_don(request, iddon):
    dons = get_object_or_404(don, iddon = iddon)  # Utilisez idMembre
    if request.method == 'POST':
        form =DonForm(request.POST, instance=dons)
        if form.is_valid():
            form.save()
            return redirect('dons')
    else:
        form = DonForm(instance=dons)
    return render(request, 'modifier_don.html', {'form': form})#
                  



def afficher_prets(request, idMembre):
    membre_instance = get_object_or_404(membre, id=idMembre)

    # Obtenir tous les prêts où le membre est un avaliste
    prets_avaliste = membre_instance.prets_en_avaliste.all()
    
    # Obtenir tous les prêts où le membre est un prêteur
    prets_preteur = membre_instance.prets_en_preteur.all()
    
    return render(request, 'afficher_prets.html', {
        'membre': membre_instance,
        'prets_avaliste': prets_avaliste,
        'prets_preteur': prets_preteur,
    })




def landing_page_view(request):
    """
    Vue simple pour afficher la page de présentation.
    """
    return render(request, 'landing.html')

