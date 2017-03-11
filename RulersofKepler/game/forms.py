from django import forms


class LobbyCreationForm(forms.Form):
    """
    Form for creating a lobby.
    """
    name = forms.CharField(max_length=255, required=False)
