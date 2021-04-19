
from .models import Comment
from django.forms import ModelForm
from django import forms

class CommentCreateForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.Textarea(attrs={
                                                                    'class': 'form-control',
                                                                    'placeholder': 'Комментарий',
                                                                    'rows': '4',
                                                                    'cols': '50'
                                                                    }))
    class Meta:
        model = Comment
        fields = ("body", )