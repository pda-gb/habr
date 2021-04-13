from django import forms

from apps.authorization.models import HabrUserProfile
from apps.articles.models import Article
from django.contrib.auth.forms import PasswordChangeForm


class HabrUserProfileEditForm(forms.ModelForm):
    class Meta:
        model = HabrUserProfile
        fields = (
            "full_name",
            "place_of_work",
            "specialization",
            "gender",
            'birth_date',
            "country",
            "region",
            "city",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ""


class ArticleCreate(forms.ModelForm):
    class Meta:
        model = Article
        fields = (
            "title",
            "hubs",
            "body",
            "image",
            "link_to_original"
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ""


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=30, label='введите старый пароль')
    new_password = forms.CharField(widget=forms.PasswordInput(), label='введите новый пароль', error_messages={'required': ''})
    repeat_password = forms.CharField(widget=forms.PasswordInput(), label='повторите пароль')

    def __init__(self, *args, **kwargs):
        # self.request = request
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = "form-control"
            field.help_text = ''

# class ChangePasswordForm(PasswordChangeForm):

# class ChangePasswordForm(forms.Form):
#     old_password = forms.PasswordField()
#     new_password = forms.PasswordField()
#     reenter_password = forms.PasswordField()
#
#     def clean(self):
#         new_password = self.cleaned_data.get('new_password')
#         reenter_password = self.cleaned_data.get('reenter_password')
#         old_password = self.cleaned_data.get('old_password')
#         if new_password and new_password != reenter_password or new_password == old_password:
#             raise forms.ValidationError('Ошибка!')
#         return self.cleaned_data
