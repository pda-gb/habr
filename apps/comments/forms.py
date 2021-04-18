
from .models import Comment
from django.forms import ModelForm
from django import forms
'''
class CommentCreateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentCreateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Comment
        fields = ("body",)
        '''

class CommentCreateForm(ModelForm):
    parent_comment = forms.IntegerField(
        widget=forms.HiddenInput,
        required=False
    )
 
    comment_area = forms.CharField(
        label="",
        widget=forms.Textarea
    )

    class Meta:
        model = Comment
        fields = ("body", )