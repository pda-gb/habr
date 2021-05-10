from django import forms
from apps.moderator.models import BannedUser


class BannedUserForm(forms.ModelForm):

    class Meta:
        model = BannedUser
        exclude = ('offender', 'date_ban', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'is_forever':
                field.widget.attrs["class"] = "checkbox-field"
            else:
                field.widget.attrs["class"] = "form-control"
            field.help_text = ""
