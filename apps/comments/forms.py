
from .models import Comment
from django.forms import ModelForm

class CommentCreateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentCreateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Comment
        fields = ("body",)