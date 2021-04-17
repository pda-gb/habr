from django import forms

from apps.authorization.models import HabrUserProfile
from apps.articles.models import Article


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
            'avatar',
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
    new_password = forms.CharField(widget=forms.PasswordInput(), label='введите новый пароль')
    repeat_password = forms.CharField(widget=forms.PasswordInput(), label='повторите пароль')

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = "form-control"
            field.help_text = ''

    def clean(self):
        super().clean()
        data_1 = self.cleaned_data['new_password']
        data_2 = self.cleaned_data['repeat_password']
        if data_1 != data_2:
            raise forms.ValidationError('Ошибка!')
        return data_1


class ArticleEditForm(forms.ModelForm):
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
        super(ArticleEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ""