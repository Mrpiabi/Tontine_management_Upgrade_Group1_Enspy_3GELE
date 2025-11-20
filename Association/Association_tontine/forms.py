from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import membre,tontines, pret,don,remboursement,Notification,versementsol,versementcotis,aide,sanction,epargne,cotisation
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from Association_tontine.models import membre


#Added New form for creation of members 

class CustomAuthenticationForm(forms.Form):
    login = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Appel correct du constructeur parent

    def clean(self):
        login = self.cleaned_data.get('login')
        password = self.cleaned_data.get('password')

        if not login or not password:
            raise forms.ValidationError("Veuillez entrer un nom d'utilisateur et un mot de passe.")

        try:
            user = membre.objects.get(login=login)
            if not check_password(password, user.password):  # Vérification du mot de passe haché
                raise forms.ValidationError("Nom d'utilisateur ou mot de passe incorrect.")
        except membre.DoesNotExist:
            raise forms.ValidationError("Nom d'utilisateur ou mot de passe incorrect.")

        return self.cleaned_data


class PasswordRegistrationForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}),
        label='Mot de passe',
        min_length=6
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmer mot de passe'}),
        label='Confirmer mot de passe',
        min_length=6
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(label='Nom d\'utilisateur', max_length=50)
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email','password']

class NotificationForm(forms.ModelForm):

    
    class Meta:
        model = Notification
        fields = ['details','statut']        

class TontineChoiceForm(forms.Form):
    tontine = forms.ModelChoiceField(
        queryset=tontines.objects.exclude(type_tontine='S'),
        label="Choisissez votre Tontine",
        empty_label="Sélectionnez une tontine",
        required=True  # Assurez-vous que le champ est requis
    )
    details = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Expliquez les raisons de votre demande',
            'rows': 4,  # Ajustez la taille du champ de texte
            'class': 'form-control'  # Ajoutez des classes CSS pour le style
        }),
        label="Détails",
        required=True  # Assurez-vous que le champ est requis
    )
    #type_modification = forms.CharField(
   #     widget=forms.HiddenInput(),
  #      initial='modification_tontine'
   # )

    def clean_details(self):
        details = self.cleaned_data.get('details')
        if not details:
            raise forms.ValidationError("Ce champ est requis.")
        return details

class MembreForm(forms.ModelForm):
    class Meta:
        model = membre
        fields = ['nom', 'prenom', 'login', 'anneeNais', 'anneeEntree', 'sexe',
                  'engagement', 'telephone1', 'telephone2', 'email',
                  'actif', 'photo', 'is_admin']
        labels = {
            'nom': 'Nom',
            'prenom': 'Prénom',
            'login': 'Identifiant',
            'anneeNais': 'Année de naissance',
            'anneeEntree': 'Année d’entrée',
            'sexe': 'Sexe',
            'engagement': 'Engagement',
            'telephone1': 'Téléphone principal',
            'telephone2': 'Téléphone secondaire',
            'email': 'Adresse email',
            'actif': 'Actif',
            'photo': 'Photo',
            'is_admin': 'Administrateur',
        }
        widgets = {
            'anneeNais': forms.NumberInput(attrs={'placeholder': 'Ex: 1990'}),
            'anneeEntree': forms.NumberInput(attrs={'placeholder': 'Ex: 2021'}),
            'email': forms.EmailInput(attrs={'placeholder': 'exemple@email.com'}),
        }

class TontinesForm(forms.ModelForm):
    class Meta:
        model = tontines    
        fields = ['nomTontines', 'montantTontine', 'Datecreation', 'type_tontine']
        labels = {
            'nomTontines': 'Nom de la Tontine',
            'montantTontine': 'Montant',
            'Datecreation': 'Date de création',
            'type_tontine': 'Type de Tontine',
        }
        widgets = {
            'Datecreation': forms.DateInput(attrs={'type': 'date'}),
        }

        

class PretForm(forms.ModelForm):
    class Meta:
        model = pret
        fields = ['idMembre_preteur', 'idMembre_avaliste', 'montant', 'pourcentage', 'date_demande','cni_avaliste']
        labels = {
            'idMembre_preteur': 'Membre Prêteur',
            'idMembre_avaliste': 'Membre Avaliste',
            'montant': 'Montant du prêt',
            'pourcentage': 'Taux d\'intérêt (%)',
            'date_demande': 'Date de la demande',
            'cni_avaliste':"Photocophie de la CNI de l'avaliste"
        }
        widgets = {
            'date_demande': forms.DateInput(attrs={'type': 'date'}),
            'avaliste': forms.Select(attrs={'class': 'form-control'}),
            'cni_avaliste': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_montant(self):
        montant = self.cleaned_data.get('montant')
        if montant and montant <= 0:
            raise forms.ValidationError("Le montant doit être supérieur à 0.")
        return montant


class DonForm(forms.ModelForm):
    class Meta:
        model = don
        fields = ['nature_don', 'montant_don', 'date_don', 'description_don', 'idTontines', 'idMembre']
        labels = {
            'nature_don': 'Nature du don',
            'montant_don': 'Montant',
            'date_don': 'Date',
            'description_don': 'Description',
            'idTontines': 'Tontine liée',
            'idMembre': 'Membre donateur',
        }
        widgets = {
            'date_don': forms.DateInput(attrs={'type': 'date'}),
            'description_don': forms.Textarea(attrs={'rows': 2}),
        }
class AideForm(forms.ModelForm):
    class Meta:
        model = aide
        fields = ['date', 'motif_aide', 'montantAide', 'nomBeneficiaire', 'lienBeneficiareAvecMembre', 'type_aide', 'lieu', 'idMembre']
        labels = {
            'date': 'Date',
            'motif_aide': 'Motif',
            'montantAide': 'Montant de l’aide',
            'nomBeneficiaire': 'Nom du bénéficiaire',
            'lienBeneficiareAvecMembre': 'Lien avec le membre',
            'type_aide': 'Type d’aide',
            'lieu': 'Lieu',
            'idMembre': 'Membre demandeur',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'motif_aide': forms.Textarea(attrs={'rows': 2}),
        }

class SanctionForm(forms.ModelForm):
    class Meta:
        model = sanction
        fields = ['dateSanction', 'typeSanction', 'montant', 'raison', 'idMembre']
        labels = {
            'dateSanction': 'Date de la sanction',
            'typeSanction': 'Type',
            'montant': 'Montant',
            'raison': 'Motif',
            'idMembre': 'Membre sanctionné',
        }
        widgets = {
            'dateSanction': forms.DateInput(attrs={'type': 'date'}),
            'raison': forms.Textarea(attrs={'rows': 2}),
        }

class RemboursementForm(forms.ModelForm):
    class Meta:
        model = remboursement
        fields = ['idpret', 'montant_rembourse', 'date_remboursement']
        labels = {
            'idpret': 'Prêt concerné',
            'montant_rembourse': 'Montant remboursé',
            'date_remboursement': 'Date de remboursement',
        }
        widgets = {
            'date_remboursement': forms.DateInput(attrs={'type': 'date'}),
        }

class VersementsolForm(forms.ModelForm):
    class Meta:
        model = versementsol
        fields = ['montant', 'modeVersement', 'couponVersement', 'idMembre', 'idSeance']
        labels = {
            'montant': 'Montant',
            'modeVersement': 'Mode de versement',
            'couponVersement': 'Coupon',
            'idMembre': 'Membre',
            'idSeance': 'Séance',
        }
class VersementcotisForm(forms.ModelForm):
    class Meta:
        model = versementcotis
        fields = ['montant', 'modeVersement', 'couponVersement', 'codeCotisation', 'idMembre', 'idSeance']
        labels = {
            'montant': 'Montant',
            'modeVersement': 'Mode de versement',
            'couponVersement': 'Coupon',
            'codeCotisation': 'Cotisation',
            'idMembre': 'Membre',
            'idSeance': 'Séance',
        }

from django.forms import TextInput, NumberInput, Select

class EpargneForm(forms.ModelForm):
    class Meta:
        model = epargne
        fields = ['montant', 'modeVersement', 'couponVersement', 'idMembre', 'idSeance']
        labels = {
            'montant': 'Montant',
            'modeVersement': 'Mode de versement',
            'couponVersement': 'Coupon',
            'idMembre': 'Membre',
            'idSeance': 'Séance',
        }
        widgets = {
            'montant': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 5000'}),
            'modeVersement': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: catch ou Numerique'}),
            'couponVersement': TextInput(attrs={'class': 'form-control', 'placeholder': 'Coupon code'}),
            'idMembre': Select(attrs={'class': 'form-select'}),
            'idSeance': NumberInput(attrs={'class': 'form-control', 'placeholder': 'seance consideree'}),
        }


class CotisationForm(forms.ModelForm):
    class Meta:
        model = cotisation
        fields = ['utilisateur','codeCotisation', 'libelle', 'nbPartMax','montant', 'idMembre', 'tontine', 'penaliteDefaillanceBenef', 'penaliteDefaillanceNonBenef', 'miseAPrix']
        labels = {
            'codeCotisation': 'Code',
            'libelle': 'Libellé',
            'nbPartMax': 'Nombre de parts max',
            'montant':'Montant de la cotisation',
            'idMembre': 'Membre',
            'tontine': 'Tontine associée',
            'penaliteDefaillanceBenef': 'Pénalité (bénéficiaire)',
            'penaliteDefaillanceNonBenef': 'Pénalité (non bénéficiaire)',
            'miseAPrix': 'Mise à prix',
        }



# Define choices here to keep them consistent
ENGAGEMENT_CHOICES = [
    ('marie(e)', 'Marié(e)'),
    ('celibataire', 'Célibataire'),
    ('divorce(e)', 'Divorcé(e)')
]
SEXE_CHOICES = [
    ('M', 'Masculin'),
    ('F', 'Féminin')
]

# THIS IS THE NEW FORM WE WILL USE TO REPLACE THE LOGIC IN 'ajouter_membre'
class SuperuserCreateMembreForm(forms.Form):
    nom = forms.CharField(max_length=50, label="Nom de famille", required=True)
    prenom = forms.CharField(max_length=50, label="Prénom(s)", required=True)
    email = forms.EmailField(
        label="Adresse Email", 
        required=True,
        help_text="Cette adresse servira aussi de nom d'utilisateur."
    )
    
    anneeEntree = forms.IntegerField(label="Année d'Entrée", required=True)
    sexe = forms.ChoiceField(choices=SEXE_CHOICES, label="Sexe")
    engagement = forms.ChoiceField(choices=ENGAGEMENT_CHOICES, label="Statut matrimonial")
    telephone1 = forms.CharField(max_length=15, label="Téléphone principal", required=True)
    
    # Optional fields from your 'membre' model
    anneeNais = forms.IntegerField(label="Année de Naissance", required=False)
    telephone2 = forms.CharField(max_length=15, label="Téléphone secondaire", required=False)

    def clean_email(self):
        """Custom validation to ensure the email is unique across the User model."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Un utilisateur avec cette adresse email existe déjà.")
        return email