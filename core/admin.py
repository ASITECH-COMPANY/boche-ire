from django.contrib import admin
from .models import Produit, Agent, Fournisseur, Client, Chauffeur, Camion, Achat, Vente, Transport, PaiementSalaire

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix_achat_moyen', 'prix_vente', 'stock_actuel')
    search_fields = ('nom',)
    list_filter = ('prix_vente',)

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'telephone', 'poste', 'date_embauche', 'salaire_base')
    search_fields = ('nom', 'prenom')
    list_filter = ('poste',)

@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'village', 'telephone', 'date_creation')
    search_fields = ('nom', 'village')
    list_filter = ('date_creation',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'type_client', 'telephone', 'produit_interesse', 'date_creation')
    search_fields = ('nom', 'prenom', 'telephone')
    list_filter = ('type_client', 'date_creation')

@admin.register(Chauffeur)
class ChauffeurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'telephone', 'ville')
    search_fields = ('nom', 'prenom', 'telephone')

@admin.register(Camion)
class CamionAdmin(admin.ModelAdmin):
    list_display = ('immatriculation', 'chauffeur', 'capacite_tonnes', 'statut')
    list_filter = ('statut',)
    search_fields = ('immatriculation',)

@admin.register(Achat)
class AchatAdmin(admin.ModelAdmin):
    list_display = ('reference', 'produit', 'fournisseur', 'agent', 'quantite', 'prix_unitaire', 'date_achat')
    search_fields = ('reference', 'produit__nom')
    list_filter = ('date_achat',)

@admin.register(Vente)
class VenteAdmin(admin.ModelAdmin):
    list_display = ('reference', 'produit', 'client', 'agent', 'quantite', 'prix_unitaire', 'montant_recu', 'reste_a_payer', 'date_vente')
    search_fields = ('reference', 'produit__nom', 'client__nom')
    list_filter = ('date_vente',)

@admin.register(Transport)
class TransportAdmin(admin.ModelAdmin):
    list_display = ('reference', 'camion', 'chauffeur', 'date_transport', 'destination', 'prix_paye')
    search_fields = ('reference', 'destination')
    list_filter = ('date_transport',)

@admin.register(PaiementSalaire)
class PaiementSalaireAdmin(admin.ModelAdmin):
    list_display = ('agent', 'date_debut', 'date_fin', 'montant', 'date_paiement', 'reference')
    search_fields = ('agent__nom', 'reference')
    list_filter = ('date_paiement',)
