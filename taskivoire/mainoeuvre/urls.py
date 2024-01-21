from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category_details/<str:category_name>', views.service_by_categorie, name='cat_detais'),
    path('service/<str:service_name>', views.prestataire_du_service, name="prestataire_du_service"),
    path('commander/client_details/<int:id_prestataire>', views.prestataire_details, name='details'),
    path('commande/<int:prestataire_id>', views.commander_prestataire, name='commande'),
    path('Dashbord_prestataire', views.prestataire_dashboard, name='dash'),
    path('Dashbord_client', views.client_dashboard, name='dash_client'),
    path('noter/<str:commande_id>', views.donner_note, name='note')
]
