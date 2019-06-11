from django import forms

from catalog.models import Person, GuestAction, HostAction

class AddGuestForm(forms.ModelForm):
    class Meta:
        model = GuestAction
        # would be better not to modify date, but I don't know how 
        # to pass date though so including it in fields
        fields = '__all__'

class ChangeHostForm(forms.ModelForm):
    class Meta:
        model = HostAction
        fields = ['host']
