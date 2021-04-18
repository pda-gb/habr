from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render

from apps.articles.models import Article
from apps.articles.models import HabrUser
from .models import Comment

#from .forms import CommentCreateForm

def get_comments(pk):
    #comment_form = CommentCreateForm(data=request.POST or None)
    comments = Comment.get_comments(article_pk=pk)
    return comments