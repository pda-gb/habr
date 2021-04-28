from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.conf import settings
from django.template.loader import render_to_string

from apps.articles.models import Article, Hub
from .forms import CommentCreateForm
from .models import Comment

@login_required
@transaction.atomic
def comment_create(request, pk):
    current_article = get_object_or_404(Article, id=pk)
    form_comment = CommentCreateForm(request.POST or None)
    if request.method == 'POST':
        if form_comment.is_valid():
            new_comment = form_comment.save(commit=False)
            new_comment.author = request.user
            new_comment.article = current_article
            new_comment.body = form_comment.cleaned_data["body"]
            new_comment.parent = None
            new_comment.is_child = False
            new_comment.save()
            #если в js стоит функция location.reload();, то return JsonResponse не нужен
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

@login_required
@transaction.atomic
def child_comment_create(request, pk, id_parent_comment):
    current_article = get_object_or_404(Article, id=pk)
    form_comment = CommentCreateForm(request.POST or None)
    if request.method == 'POST':
        if form_comment.is_valid():
            new_comment = form_comment.save(commit=False)
            new_comment.author = request.user
            new_comment.article = current_article
            new_comment.body = form_comment.cleaned_data["body"]
            new_comment.parent = Comment.get_comment(id_parent_comment)
            new_comment.is_child = True
            new_comment.save()
            #если в js стоит функция location.reload();, то return JsonResponse не нужен
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
