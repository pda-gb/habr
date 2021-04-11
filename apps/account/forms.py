from django import forms
from django.contrib.auth.forms import UserChangeForm
from apps.authorization.models import HabrUser, HabrUserProfile


class HabrUserEditForm(UserChangeForm):
    class Meta:
        model = HabrUser
        fields = ('username', 'first_name', 'email', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def __str__(self):
        return self.fields['avatar']


class HabrUserProfileEditForm(forms.ModelForm):
    class Meta:
        model = HabrUserProfile
        fields = ('full_name', 'place_of_work', 'specialization', 'gender', 'country', 'region', 'city')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
