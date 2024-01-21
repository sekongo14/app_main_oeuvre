from django.urls import  path
from . import views

urlpatterns = [
    path('prestataire_singup', views.prestataire_signup, name='prestForm'),
    path('client_signup', views.Client_signup, name='clientForm'),
    path('login', views.signin, name='login'),
    path('deconexion', views.logout_user, name='deco')
]
