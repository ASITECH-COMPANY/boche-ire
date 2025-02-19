# models.py
from django.db import models
from django.utils import timezone
import uuid

class Produit(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    prix_achat_moyen = models.DecimalField(max_digits=10, decimal_places=2)
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2)
    stock_actuel = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return self.nom
    
    def calculer_marge(self):
        return self.prix_vente - self.prix_achat_moyen
    
    def calculer_marge_pourcentage(self):
        if self.prix_achat_moyen == 0:
            return 0
        return ((self.prix_vente - self.prix_achat_moyen) / self.prix_achat_moyen) * 100

class Agent(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    adresse = models.TextField()
    poste = models.CharField(max_length=50)
    date_embauche = models.DateField()
    salaire_base = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100, blank=True, null=True)
    village = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    date_creation = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    km_a_parakou = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    def __str__(self):
        if self.prenom:
            return f"{self.prenom} {self.nom} - {self.village}"
        return f"{self.nom} - {self.village}"

class Client(models.Model):
    TYPE_CHOICES = [
        ('entreprise', 'Entreprise'),
        ('particulier', 'Particulier'),
    ]
    
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100, blank=True, null=True)
    type_client = models.CharField(max_length=15, choices=TYPE_CHOICES, default='particulier')
    telephone = models.CharField(max_length=20)
    adresse = models.TextField()
    produit_interesse = models.ForeignKey(Produit, on_delete=models.SET_NULL, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.type_client == 'entreprise':
            return f"{self.nom} (Entreprise)"
        return f"{self.prenom} {self.nom}"

class Chauffeur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    ville = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Camion(models.Model):
    STATUT_CHOICES = [
        ('disponible', 'Disponible'),
        ('en_mission', 'En Mission'),
        ('en_maintenance', 'En Maintenance'),
    ]
    
    immatriculation = models.CharField(max_length=20, unique=True)
    chauffeur = models.ForeignKey(Chauffeur, on_delete=models.SET_NULL, null=True, blank=True)
    capacite_tonnes = models.DecimalField(max_digits=6, decimal_places=2)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='disponible')
    
    def __str__(self):
        return f"{self.immatriculation} - {self.chauffeur if self.chauffeur else 'Sans chauffeur'}"

class Achat(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    quantite = models.DecimalField(max_digits=10, decimal_places=2)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    prix_transport = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_achat = models.DateField()
    reference = models.CharField(max_length=20, unique=True, default=uuid.uuid4)
    km_a_parakou = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    observation = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Achat #{self.reference} - {self.produit.nom} ({self.quantite})"
    
    def montant_total(self):
        return (self.quantite * self.prix_unitaire) + self.prix_transport
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Mettre à jour le stock
        self.produit.stock_actuel += self.quantite
        self.produit.save()

class Vente(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    quantite = models.DecimalField(max_digits=10, decimal_places=2)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    montant_recu = models.DecimalField(max_digits=10, decimal_places=2)
    reste_a_payer = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_vente = models.DateField()
    reference = models.CharField(max_length=20, unique=True, default=uuid.uuid4)
    observation = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Vente #{self.reference} - {self.produit.nom} ({self.quantite})"
    
    def montant_total(self):
        return self.quantite * self.prix_unitaire
    
    def save(self, *args, **kwargs):
        # Calculer le reste à payer
        total = self.montant_total()
        self.reste_a_payer = total - self.montant_recu
        
        super().save(*args, **kwargs)
        
        # Mettre à jour le stock
        self.produit.stock_actuel -= self.quantite
        self.produit.save()

class Transport(models.Model):
    camion = models.ForeignKey(Camion, on_delete=models.CASCADE)
    chauffeur = models.ForeignKey(Chauffeur, on_delete=models.CASCADE)
    date_transport = models.DateField()
    destination = models.CharField(max_length=100)
    prix_paye = models.DecimalField(max_digits=10, decimal_places=2)
    achat = models.ForeignKey(Achat, on_delete=models.SET_NULL, null=True, blank=True)
    vente = models.ForeignKey(Vente, on_delete=models.SET_NULL, null=True, blank=True)
    reference = models.CharField(max_length=20, unique=True, default=uuid.uuid4)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Transport #{self.reference} - {self.destination} ({self.date_transport})"

class PaiementSalaire(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin = models.DateField()
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateField()
    reference = models.CharField(max_length=20, unique=True, default=uuid.uuid4)
    
    def __str__(self):
        return f"Salaire {self.agent} - {self.date_debut} à {self.date_fin}"
    
    class Meta:
        verbose_name = "Paiement de salaire"
        verbose_name_plural = "Paiements de salaires"
        