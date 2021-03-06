from django.conf import settings
from django.db import transaction
from django.http.response import JsonResponse
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from apps.articles.models import Article, Hub
from apps.authorization.models import HabrUser
from .forms import CommentCreateForm
from .models import Comment
from .utils import create_comments_tree


@login_required
def create_comment(request, pk):
    current_article = get_object_or_404(Article, id=pk)
    form_comment = CommentCreateForm(request.POST or None)
    if form_comment.is_valid():
        new_comment = form_comment.save(commit=False)
        new_comment.author = request.user
        new_comment.article = current_article
        new_comment.body = form_comment.cleaned_data["body"]
        new_comment.parent = None
        new_comment.is_child = False
        new_comment.save()
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
@transaction.atomic
def create_child_comment(request, pk):
    user_name = request.user.username
    current_id = request.POST.get("id")
    current_article = get_object_or_404(Article, id=pk)
    text = request.POST.get("text")
    user = HabrUser.objects.get(username=user_name)
    parent = Comment.objects.get(id=int(current_id))
    is_child = False if not parent else True

    hubs_menu = Hub.get_all_hubs()
    last_articles = Article.get_last_articles(Article.get_articles())
    form_comment = CommentCreateForm(request.POST or None)

    Comment.objects.create(
        article=current_article,
        author=user,
        body=text,
        parent=parent,
        is_child=is_child,
    )

    comments_ = Comment.get_comments(pk)
    comments_list = create_comments_tree(comments_)
    page_data = {
        "article": current_article,
        "hubs_menu": hubs_menu,
        "form_comment": form_comment,
        "last_articles": last_articles,
        "media_url": settings.MEDIA_URL,
        "comments": comments_list,
    }
    result = render_to_string("comments/comments.html", page_data)
    return JsonResponse({"result": result})


def like_dislike_ajax(request):
    if request.is_ajax() and request.user.is_authenticated:
        field = request.GET.get("field")
        comment = request.GET.get("comment").split("-")[1]
        comment = Comment.objects.get(pk=comment)
        if request.user != comment.author:
            if field == "like":
                if comment.likes.filter(pk=request.user.pk).exists():
                    comment.likes.remove(request.user)
                    comment.author.habruserprofile.rating -= 1 * 0.5
                elif comment.dislikes.filter(pk=request.user.pk).exists():
                    comment.likes.add(request.user)
                    comment.dislikes.remove(request.user)
                    comment.author.habruserprofile.rating += 2 * 0.5
                else:
                    comment.likes.add(request.user)
                    comment.author.habruserprofile.rating += 1 * 0.5
            elif field == "dislike":
                if comment.dislikes.filter(pk=request.user.pk).exists():
                    comment.dislikes.remove(request.user)
                    comment.author.habruserprofile.rating += 1 * 0.5
                elif comment.likes.filter(pk=request.user.pk).exists():
                    comment.dislikes.add(request.user)
                    comment.likes.remove(request.user)
                    comment.author.habruserprofile.rating -= 2 * 0.5
                else:
                    comment.dislikes.add(request.user)
                    comment.author.habruserprofile.rating -= 1 * 0.5
            comment.author.habruserprofile.save()
        return JsonResponse(
            {
                "id": comment.pk,
                "likes": comment.likes.count(),
                "dislikes": comment.dislikes.count(),
                "like": comment.likes.filter(pk=request.user.pk).exists(),
                "dislike": comment.dislikes.filter(pk=request.user.pk).exists(),
            }
        )
