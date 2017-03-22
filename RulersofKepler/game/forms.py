from django import forms
from django.core.validators import RegexValidator


class LobbyCreationForm(forms.Form):
    """
    Form for creating a lobby and a regexvalidator to check the name.
    """
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    name = forms.CharField(max_length=255, required=False, validators=[alphanumeric])
