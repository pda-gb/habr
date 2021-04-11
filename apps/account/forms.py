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
