from django import forms

from catalog.models import Person, GuestAction, HostAction

class AddPersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'active']

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

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = HostAction
        fields = ['comment']
