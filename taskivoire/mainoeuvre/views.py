from django.shortcuts import render, get_object_or_404, redirect
from .models import CategoryService, Prestataire, Client, Service, Commande
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .forms import NoteForm
# Create your views here.
def index(request):
    data = CategoryService.objects.all()[:3]
    prest = Prestataire.objects.all()
    return render(request, 'gestion/index.html', {'data':data, 'prest':prest})

def service_by_categorie(request, category_name):
    category = get_object_or_404(CategoryService, nom=category_name)
    # Récupérer les services associés à la catégorie
    services = Service.objects.filter(category=category)
    # Initialiser une liste pour stocker les prestataires associés à tous les services
    prestataires = []
    # Boucler sur les services pour récupérer les prestataires associés à chaque service
    for service in services:
        prestataires_du_service = Prestataire.objects.filter(services=service)
        prestataires.extend(prestataires_du_service)
    return render(request, 'gestion/category_detail.html', {'category': category, 'services': services, 'prestataires': prestataires})


def prestataire_du_service(request, service_name = None):
    prest = Prestataire.objects.all()
    if service_name :
        service = get_object_or_404(Service, nom = service_name)
        prest = prest.filter(services = service)
    paginator = Paginator(prest, 2)
    page = request.GET.get('page')
    try:
        prest = paginator.page(page)   
    except PageNotAnInteger:
        prest = paginator.page(1)
    except EmptyPage:
            prest = paginator.page(paginator.num_pages)     
    context = {
        'prest': prest,
        'page': page,
        'service': service,
    }        
    return render(request, 'gestion/prest_du_service.html', context)


# def commander_prestataire(request, prestataire_id):
#     prestataire = get_object_or_404(Prestataire, id=prestataire_id)

#     if request.method == 'POST':
#         # Créer une nouvelle commande
#         Commande.objects.create(
#             client=request.user.client,
#             prestataire=prestataire,
#             # Vous pouvez définir l'état initial de la commande ici
#         )
#          # Envoyer une notification par e-mail au prestataire
#         # sujet = f"Nouvelle commande de {commande.client.user.prenom} {commande.client.user.nom}"
#         # message = f"Bonjour {prestataire.user.prenom}, vous avez une nouvelle commande de {commande.client.user.prenom} {commande.client.user.nom}."
#         # destinataires = [prestataire.user.email]  # Assurez-vous que le modèle CustomUser a un champ email

#         # send_mail(sujet, message, 'sekongoismael0@gmail.com', destinataires)

#     context = {'prestataire': prestataire}
#     return redirect('index')
def commander_prestataire(request, prestataire_id):
    prestataire = get_object_or_404(Prestataire, id=prestataire_id)

    if request.method == 'POST':
        # Créer une nouvelle commande
        commande = Commande.objects.create(
            client=request.user.client,
            prestataire=prestataire,
            # Vous pouvez définir l'état initial de la commande ici
        )
        # Envoyer une notification par e-mail au prestataire
        # sujet = f"Nouvelle commande de {commande.client.user.last_name} {commande.client.user.first_name}"
        # message = f"Bonjour {prestataire.user.last_name}, vous avez une nouvelle commande de {commande.client.user.last_name} {commande.client.user.first_name}."
        # destinataires = [prestataire.user.email]  # Assurez-vous que le modèle CustomUser a un champ email

        # send_mail(sujet, message, 'gninningafolosekongo@gmail.com', destinataires)

    return redirect('index')

@login_required(login_url='login')
def prestataire_dashboard(request):
    prestataire = request.user.prestataire  # Obtenez l'instance Prestataire associée à l'utilisateur connecté
    commandes = Commande.objects.filter(prestataire=request.user.prestataire)
    moyenne_notes = prestataire.calculer_moyenne_notes()
    return render(request, 'gestion/prestataire_dashboard.html', {'prestataire': prestataire, 'commandes':commandes, 'moy':moyenne_notes})

@login_required(login_url='login')
def client_dashboard(request):
    client = request.user.client  # Obtenez l'instance Prestataire associée à l'utilisateur connecté
    commandes = Commande.objects.filter(client=request.user.client)
    return render(request, 'gestion/client_dashboard.html', {'client': client, 'commandes':commandes})


def prestataire_details(request, id_prestataire):
    prestataire = get_object_or_404(Prestataire, id=id_prestataire)
    note = prestataire.calculer_moyenne_notes()
    return render(request, 'gestion/details.html', {'prestataire': prestataire, 'moyenne':note})


def donner_note(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=commande)
        if form.is_valid():
            form.save()
            return redirect('dash_client')
    else:
        form = NoteForm(instance=commande)

    return render(request, 'gestion/Note.html', {'form': form, 'commande': commande})