from django import forms

from catalog.models import Person, GuestAction
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class AddGuestForm(forms.ModelForm):
    class Meta:
        model = GuestAction
        fields = '__all__'

