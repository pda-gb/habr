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
            if request.is_ajax():
                comments_list = Comment.get_comments(pk)
                hubs_menu = Hub.get_all_hubs()
                last_articles = Article.get_last_articles(Article.get_articles())
                content = {
                    "articles": current_article,
                    "hubs_menu": hubs_menu,
                    "form_comment": form_comment,
                    "last_articles": last_articles,
                    "media_url": settings.MEDIA_URL,
                    "comments": comments_list,
                }
                result = render_to_string("comments/includes/comments_list.html", content)
                print(result)
                return JsonResponse({'result':result})
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

@login_required
@transaction.atomic
def child_comment_create(request, pk, id_parent_comment):
    user_name = request.user
    text = request.POST.get("body")
    Comment.create_comment(int(pk), int(id_parent_comment), user_name, text)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
