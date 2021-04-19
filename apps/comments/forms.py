
from .models import Comment
from django.forms import ModelForm
from django import forms

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body", )