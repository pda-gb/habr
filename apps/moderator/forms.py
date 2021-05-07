from django import forms
from apps.moderator.models import BannedUser


class BannedUserForm(forms.Form):
    SPAM = (
        (True, 'да'),
        (False, 'нет'),
    )
    # class Meta:
    #     model = BannedUser
    #     exclude = ('offender', 'date_ban', 'is_active')
    reason = forms.CharField(widget=forms.Textarea, label="Причина блокировки")
    num_days = forms.CharField(widget=forms.NumberInput, label="Дней блокировки")
    # is_forever = forms.NullBooleanField(required=False, label='Блокировать навсегда')
    is_forever = forms.TypedChoiceField(widget=forms.Select, choices=SPAM, label='Блокировать навсегда')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ""
