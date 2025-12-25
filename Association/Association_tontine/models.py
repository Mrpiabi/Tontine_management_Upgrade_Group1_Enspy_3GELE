from django.db import models  # Si vous utilisez le modèle User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry
from django.conf import settings

    

class membre(models.Model):
    idMembre = models.BigAutoField(db_column='idMembre', primary_key=True)
    nom = models.CharField(db_column='nom', max_length=50, blank=True, null=True)
    prenom = models.CharField(db_column='prenom', max_length=50, blank=True, null=True)
    anneeNais = models.SmallIntegerField(db_column='anneeNais', blank=True, null=True)
    anneeEntree = models.SmallIntegerField(blank=True, null=True)
    #nbDeFemmes = models.IntegerField(db_column='nbDeFemmes')
    login = models.CharField(db_column='login', max_length=50, unique=True)
    #last_login = models.DateTimeField(null=True, blank=True) 
    #password=models.CharField(db_column='password', max_length=128, blank=True, null=True)
    sexe = models.CharField(max_length=1)
    #nomEpoux = models.CharField(db_column='nomEpoux', max_length=50, blank=True, null=True)
    engagement = models.CharField(max_length=50, choices=[('marie(e)', 'Marie(e)'), ('celibataire', 'Celibataire'),('divorce(e)','Divorce(e)')])
    telephone1 = models.CharField(max_length=15, blank=True, null=True)
    telephone2 = models.CharField(max_length=15, blank=True, null=True)
    #typeTontine = models.ForeignKey(TypeTontine,on_delete=models.CASCADE)
    email = models.EmailField(max_length=50, blank=True, null=True)
    actif = models.IntegerField(blank=True, null=True)
    photo = models.CharField(max_length=50, blank=True, null=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,related_name='membre')
    is_admin = models.BooleanField(default=False)  # Champ pour vérifier si c'est un administrateur
    #tontine = models.ForeignKey(tontines, on_delete=models.CASCADE,related_name='membres')


    
    class Meta:
        db_table = 'membre'
    def __str__(self):
        return self.user.username  




class tontines(models.Model):
    idTontines = models.AutoField(db_column='idTontines', primary_key=True)
    nomTontines = models.CharField(db_column='nomTontines', max_length=45)
    #idMembre = models.ForeignKey(membre, on_delete=models.CASCADE,db_column='idMembre',related_name='tontines')
    montantTontine = models.DecimalField(db_column='montantTontine', max_digits=20, decimal_places=5)
    libelle = models.CharField(max_length=500)  # Exemple de champ
    Datecreation = models.DateField(db_column='dateCreation', blank=True, null=True)
    TYPE_CHOICES = [
        ('S', 'Tontine Spéciale Journalière'),  # Tontine spéciale
        ('A', 'Tontine A 2000'),
        ('B', 'Tontine B 5000'),
        ('C', 'Tontine C 10000'),
        ('D', 'Tontine D 100000'),
    ]
    type_tontine = models.CharField(max_length=1, choices=TYPE_CHOICES)
    montant_obligatoire = models.DecimalField(max_digits=10, decimal_places=2, default=1000)
    membres = models.ManyToManyField(membre, through='TontinesMembres', related_name='tontines')
     # Méthode pour afficher le nom de la tontine
    def __str__(self):
        return self.nomTontines

    class Meta:
        db_table = 'tontines'    

'''class Notification(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    type_modification = models.CharField(max_length=100)  # ex: 'tontine', 'pret'
    details = models.TextField()  # JSONField si Django 3.1+ (préfèrable)
    statut = models.CharField(
        max_length=20,
        choices=[('en_attente', 'En Attente'), ('valide', 'Validé'), ('refuse', 'Refusé')],
        default='en_attente'
    )
    date_envoi = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.utilisateur.username} - {self.type_modification} - {self.statut} - {self.details} "
'''

class Demande(models.Model):
    """
    A single, unified model to handle all change requests from users.
    Renamed from DemandeModification for clarity.
    """
    # CHOICES for the type of request
    TYPE_CHOIX = [
        ('TONTINE', 'Adhésion Tontine'),
        ('PRET', 'Demande de Prêt'),
        ('REMBOURSEMENT', 'Déclaration de Remboursement'),
    ]
    
    # CHOICES for the status of the request
    STATUT_CHOIX = [
        ('EN_ATTENTE', 'En Attente'),
        ('VALIDEE', 'Validée'),
        ('REFUSEE', 'Refusée'),
    ]

    # The user who made the request.
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="demandes")
    
    # The type of request, using the choices defined above.
    type_demande = models.CharField(max_length=20, choices=TYPE_CHOIX)
    
    # The data associated with the request, stored in a structured JSON format.
    donnees = models.JSONField()
    
    # The current status of the request.
    statut = models.CharField(max_length=20, choices=STATUT_CHOIX, default='EN_ATTENTE')
    
    # Timestamps for tracking
    date_creation = models.DateTimeField(auto_now_add=True)
    date_traitement = models.DateTimeField(null=True, blank=True) # Will be set when an admin acts on it
    
    # Optional field for the admin to leave a comment (e.g., reason for refusal)
    commentaire_admin = models.TextField(blank=True, null=True)
    
    # The admin who processed the request
    traitee_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="demandes_traitees")

    def __str__(self):
        return f"Demande de {self.get_type_demande_display()} par {self.utilisateur.username} - Statut: {self.get_statut_display()}"

    class Meta:
        ordering = ['-date_creation'] # Show the newest requests first   
       

    
    
class TontinesMembres(models.Model):
    tontines = models.ForeignKey(tontines, on_delete=models.CASCADE)
    membres = models.ForeignKey(membre, on_delete=models.CASCADE)
    date_entree = models.DateField(auto_now_add=True, null=True)
    numero_adhesion = models.PositiveIntegerField()
    class Meta:
        db_table = 'tontines_membres'
        constraints = []


# Modèle pour Aide
class aide(models.Model):
    
    numAide = models.AutoField(db_column='numAide', primary_key=True)
    date = models.DateField(db_column='date', blank=True, null=True)
    motif_aide = models.CharField(db_column='motif_aide', max_length=50, blank=True, null=True)
    montantAide = models.DecimalField(db_column='montantAide', max_digits=15, decimal_places=2)
    nomBeneficiaire = models.CharField(db_column='nomBeneficiaire', max_length=50)
    lienBeneficiareAvecMembre = models.CharField(db_column='lienBeneficiareAvecMembre', max_length=50)
    type_aide = models.CharField(db_column='type_aide', max_length=50, blank=True, null=True)
    idMembre = models.ForeignKey(membre, on_delete=models.CASCADE,db_column='idMembre',related_name='aides')
    lieu = models.CharField(db_column='lieu', max_length=255, blank=True, null=True)
    

    def __str__(self):
        return f"Aide de {self.montant} pour {self.membre.nom}"
    class Meta:
        db_table = 'aide'


# Modèle pour Cotisation
class cotisation(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    codeCotisation = models.BigAutoField(db_column='codeCotisation', primary_key=True)
    libelle = models.CharField(max_length=15)
    montant = models.DecimalField(max_digits=19, decimal_places=4)
    date_paiement = models.DateField(db_column='date_paiement', blank=True)
    est_valide = models.BooleanField(default=False)  # Pour validation par l'administrateur
    nbPartMax = models.IntegerField(db_column='nbPartMax', blank=True, null=True)
    penaliteDefaillanceBenef = models.DecimalField(db_column='penaliteDefaillanceBenef', max_digits=15, decimal_places=2, blank=True, null=True)
    penaliteDefaillanceNonBenef = models.DecimalField(db_column='penaliteDefaillanceNonBenef', max_digits=15, decimal_places=2, blank=True, null=True)
    miseAPrix = models.DecimalField(db_column='miseAPrix', max_digits=19, decimal_places=4)
    idMembre = models.ForeignKey(membre, on_delete=models.CASCADE,db_column='idMembre',related_name='cotisations')
    tontine = models.ForeignKey(tontines, on_delete=models.CASCADE,db_column='tontines')
    
    def __str__(self):
        return f"Cotisation de {self.montant} pour la tontine {self.tontine.nomTontines}"
    class Meta:
        db_table = 'cotisation'


# Modèle pour Epargne
class epargne(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    idEpargne = models.AutoField(db_column='idEpargne', primary_key=True)
    montant = models.DecimalField(max_digits=19, decimal_places=4)
    modeVersement = models.CharField(db_column='modeVersement', max_length=20)
    couponVersement = models.CharField(db_column='couponVersement', unique=True, max_length=64, blank=True, null=True)
    idMembre = models.ForeignKey(membre, on_delete=models.CASCADE,db_column='idMembre',related_name='epargnes')
    idSeance = models.BigIntegerField(db_column='idSeance')

    def __str__(self):
        return f"Epargne de {self.montant} par {self.membre.nom}"
    class Meta:
        db_table = 'epargne'




# Modèle pour Pret
class pret(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    idpret = models.BigAutoField(db_column='idpret', primary_key=True)
    montant = models.DecimalField(max_digits=15, decimal_places=2)
    observations = models.TextField(blank=True, null=True)
    date_demande = models.DateTimeField()
    statut = models.CharField(max_length=50, choices=[('en_cours', 'En Cours'), ('rembourse', 'Remboursé')])
    pourcentage = models.DecimalField(max_digits=15, decimal_places=2)
    idMembre_avaliste = models.ForeignKey(membre, related_name='prets_avaliste', on_delete=models.CASCADE)
    cni_avaliste = models.FileField(upload_to='documents_cni/', null=True, blank=True)
    idSeance = models.BigIntegerField(db_column='idSeance', null=True, blank=True)
    idMembre_preteur = models.ForeignKey(membre, related_name='prets_preteur', on_delete=models.CASCADE)
    idSeance_1 = models.BigIntegerField(db_column='idSeance_1', null=True, blank=True)
    est_rembourse = models.BooleanField(default=False)
    def montant_restant(self):
        total_rembourse = sum(remboursement.montant_rembourse for remboursement in self.remboursements.all())
        montant_total = self.montant + (self.montant * self.pourcentage / 100)
        return montant_total - total_rembourse
    def est_en_cours_remboursement(self):
        return not self.est_rembourse and self.montant_restant() > 0
    def __str__(self):
        return f"Prêt de {self.montant} par {self.idMembre_preteur.nom} avec avaliste {self.idMembre_avaliste.nom}"
    class Meta:
        db_table = 'pret'


# Modèle pour Remboursement
class remboursement(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    idRembo = models.BigAutoField(db_column='idRembo', primary_key=True)
    montant_rembourse = models.DecimalField(max_digits=15, decimal_places=2)
    idpret = models.ForeignKey(pret, on_delete=models.CASCADE,db_column='idpret', related_name='remboursements')
    date_remboursement = models.DateTimeField()
    idSeance=models.BigIntegerField(db_column='idSeance')
    idMembre = models.ForeignKey(membre, on_delete=models.CASCADE, db_column='idMembre',related_name='remboursements')
    
    def __str__(self):
        return f"Remboursement de {self.montant} pour {self.pret.membre.nom}"
    class Meta:
        db_table = 'remboursement'
# Modèle pour Sanction
class sanction(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    idSanction = models.AutoField(db_column='idSanction', primary_key=True)
    dateSanction = models.DateField(db_column='dateSanction')
    typeSanction = models.CharField(db_column='typeSanction', max_length=50)
    montant = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    raison = models.TextField()
    idMembre = models.ForeignKey(membre, on_delete=models.CASCADE,db_column='idMembre',related_name='sanctions')
   
    def __str__(self):
        return f"Sanction pour {self.membre.nom}: {self.raison}"
    class Meta:
        db_table = 'sanction'


# Modèle pour versementcotis
class versementcotis(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    idVersCotis = models.AutoField(db_column='idVersCotis', primary_key=True)
    montant = models.DecimalField(max_digits=15, decimal_places=2)
    modeVersement = models.CharField(db_column='modeVersement', max_length=20)
    couponVersement = models.CharField(db_column='couponVersement', unique=True, max_length=64, blank=True, null=True)
    idMembre = models.ForeignKey(membre, on_delete=models.CASCADE,db_column='idMembre')
    codeCotisation = models.ForeignKey(cotisation, on_delete=models.CASCADE, db_column='codeCotisation',related_name='versementcotisa')
    idSeance = models.BigIntegerField(db_column='idSeance')

    def __str__(self):
            return f"Versement de cotisation de {self.montant} par {self.membre.nom}"
    class Meta:
        db_table = 'versementcotis'


# Modèle pour versementsol
class versementsol(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    idVersSol = models.AutoField(db_column='idVersSol', primary_key=True)
    montant = models.DecimalField(max_digits=15, decimal_places=2)
    modeVersement = models.CharField(db_column='modeVersement', max_length=20)
    couponVersement = models.CharField(db_column='couponVersement', unique=True, max_length=64, blank=True, null=True)
    idMembre = models.ForeignKey(membre, on_delete=models.CASCADE,db_column='idMembre',related_name='versementsols')
    idSeance = models.BigIntegerField(db_column='idSeance')

    def __str__(self):
        return f"Versement de {self.montant} par {self.membre.nom}"
    class Meta:
        db_table = 'versementSol'


class don(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    iddon = models.AutoField(db_column='iddon', primary_key=True)  # Si vous avez un ID auto-incrémenté
    nature_don = models.CharField(max_length=255)
    date_don = models.DateField()
    montant_don = models.DecimalField(max_digits=10, decimal_places=2)
    description_don = models.CharField(max_length=255)    
    idTontines = models.ForeignKey(tontines, on_delete=models.CASCADE, db_column='idTontines')
    idMembre = models.ForeignKey(membre, on_delete=models.CASCADE,db_column='idMembre',related_name='dons')
    
    def __str__(self):
        return f"{self.membre.nom} - {self.montant}"
    class Meta:
        db_table = 'don'  # Nom de la table dans la base de données