from django import forms
from apps.moderator.models import BannedUser

class BannedUserForm(forms.ModelForm):

    class Meta:
        model = BannedUser

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field
