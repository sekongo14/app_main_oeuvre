from django.shortcuts import render, redirect
from .forms import PrestataireSignUpForm, PrestataireProfileForm, ClientSignUpForm, CustomAuthenticationForm
from mainoeuvre.models import Prestataire, Client
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
# Create your views here.

def prestataire_signup(request):
    if request.method == 'POST':
        form = PrestataireSignUpForm(request.POST)
        profile_form = PrestataireProfileForm(request.POST, request.FILES)

        if form.is_valid() and profile_form.is_valid():
            user = form.save(commit=False)
            user.is_prestataire = True
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

          # Redirection de  l'utilisateur après l'inscription
        return redirect('index')
    else:
        form = PrestataireSignUpForm()
        profile_form = PrestataireProfileForm()

    return render(request, 'compte/Prestataire_signup.html', {'form': form, 'profil_form': profile_form})

def Client_signup(request):
    if request.method == 'POST':
        form = ClientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit= False)
            user.is_commandeur = True
            user.save()

            Client.objects.create(
                user=user,
                ville= form.cleaned_data['ville'],
                quartier= form.cleaned_data['quartier']
            )

        return redirect('index')
    else:
        form = ClientSignUpForm()
    return render(request, 'compte/client_signup.html', {"form":form})    


def signin(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = CustomAuthenticationForm()
    return render(request, "compte/login.html", {'form': form})


def logout_user(request):
    logout(request)
    return redirect('index')
    