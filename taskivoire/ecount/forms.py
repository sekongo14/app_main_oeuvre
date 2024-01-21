from django import forms
from django.contrib.auth.forms import UserCreationForm
from mainoeuvre.models import CustomUser, Service, Prestataire, Client, Ville, Quartier, Commande
from django.contrib.auth.forms import AuthenticationForm

class PrestataireSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'numero', 'password1', 'password2']

class PrestataireProfileForm(forms.ModelForm):
    class Meta:
        model = Prestataire
        fields = ['photo', 'prix', 'services', 'ville', 'quartier'] 



class ClientSignUpForm(UserCreationForm):
    ville = forms.ModelChoiceField(
        queryset=Ville.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    quartier = forms.ModelChoiceField(
        queryset=Quartier.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    class Meta:
        model = CustomUser
        fields = ['username',  'first_name', 'last_name', 'email', 'ville', 'quartier', 'numero', 'password1', 'password2']


class NoteForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['note']        


class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': (
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': ("This account is inactive."),
    }

    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={ 'class' : 'input100', 'type' : 'text', 'name' : 'email'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class' : 'input100', 'type' : 'password', 'name': 'pass'}),
    )        