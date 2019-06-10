from django import forms
from catalog.models import Person, GuestAction

class AddGuestForm(forms.ModelForm):
    class Meta:
        model = GuestAction
        fields = '__all__'
