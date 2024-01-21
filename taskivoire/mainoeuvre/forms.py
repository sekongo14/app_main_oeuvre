from django import forms
from .models import Commande


class NoteForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['note']        