from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Ville(models.Model):
    nom = models.CharField(max_length=30)

    def __str__(self):
        return self.nom

class Quartier(models.Model):
    nom = models.CharField(max_length=30)

    def __str__(self):
        return self.nom
  
class CustomUser(AbstractUser):
    is_prestataire = models.BooleanField(default=False)
    is_commandeur = models.BooleanField(default=False)
    numero = models.CharField(max_length=15)
  

    def __str__(self):
        return f"{self.username} {self.first_name} {self.last_name}"

class CategoryService(models.Model):
    nom = models.CharField(max_length=100, default='Maison')
    description = models.TextField(max_length=400, null=True)
    def __str__(self) -> str:
        return self.nom
    

class Service(models.Model):
    nom = models.CharField(max_length=60, default = 'peintre')
    category = models.ForeignKey(CategoryService, on_delete= models.CASCADE)

    def __str__(self) -> str:
        return self.nom


class Prestataire(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    services = models.ForeignKey(Service, on_delete= models.CASCADE, default = None)
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE, default=1)
    quartier = models.ForeignKey(Quartier, on_delete=models.CASCADE, default=1)
    prix = models.IntegerField()
    photo = models.ImageField(upload_to='photo')
    est_disponible = models.BooleanField(default=True)

    def calculer_moyenne_notes(self):
        commandes = Commande.objects.filter(prestataire=self)
        notes = [commande.note for commande in commandes if commande.note is not None]
        
        if notes:
            moyenne = sum(notes) / len(notes)
            return moyenne
        else:
            return None

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}" 

class Client(models.Model):  
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE, default=1)
    quartier = models.ForeignKey(Quartier, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.user.username}"

class Commande(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    prestataire = models.ForeignKey(Prestataire, on_delete=models.CASCADE)
    date_commande = models.DateTimeField(auto_now_add=True)
    note = models.IntegerField(blank=True, null=True)
    est_disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"Commande de {self.client} à {self.prestataire} le {self.date_commande}"
    
