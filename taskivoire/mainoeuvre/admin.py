from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Service, CategoryService, Prestataire, Ville, Quartier, Client, Commande

# admin.site.register(CustomUser, UserAdmin)

@admin.register(Ville)
class VilleAdmin(admin.ModelAdmin):
     list_display = ['nom',]

@admin.register(Quartier)
class QuartierAdmin(admin.ModelAdmin):
     list_display = ['nom',]     

@admin.register(CustomUser)
class CustumAdmin(admin.ModelAdmin):
        list_display = ['first_name', 'last_name', 'is_prestataire', 'is_commandeur','password']

@admin.register(Prestataire)
class PrestataireAdmin(admin.ModelAdmin):
    list_display = ['user', 'services', 'prix', 'photo',  'ville', 'quartier']

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['user', 'ville', 'quartier']


@admin.register(CategoryService)
class CategoryAdmin(admin.ModelAdmin):
    list_display =['nom',]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display =['nom',]    


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
     list_display= ['client', 'prestataire', 'note']