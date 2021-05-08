from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from apps.articles.models import Article, LikesViewed, DislikesViewed
from apps.authorization.models import HabrUser, KarmaPositiveViewed, KarmaNegativeViewed
from apps.authorization.models import HabrUserProfile
from apps.comments.forms import CommentCreateForm
from apps.comments.models import Comment, Sorted
from apps.comments.utils import create_comments_tree
from apps.moderator.models import BannedUser


def main_page(request, pk=None, page=1):
    """рендер главной страницы"""
    title = "главная страница"

    if pk is None:
        hub_articles = Article.get_articles()
    else:
        hub_articles = Article.get_by_hub(pk)

    last_articles = Article.get_last_articles(hub_articles)
    if request.user.is_authenticated:
        notifications = notification(request)
    else:
        notifications = None
    paginator = Paginator(hub_articles, 5)
    try:
        articles_paginator = paginator.page(page)
    except PageNotAnInteger:
        articles_paginator = paginator.page(1)
    except EmptyPage:
        articles_paginator = paginator.page(paginator.num_pages)

    page_data = {
        "title": title,
        "articles": articles_paginator,
        "last_articles": last_articles,
        "current_user": request.user,
        "notifications": notifications,
    }
    return render(request, "articles/articles.html", page_data)


def hub(request, pk=None, page=1):
    if pk is None:
        hub_articles = Article.get_articles()
    else:
        hub_articles = Article.get_by_hub(pk)

    last_articles = Article.get_last_articles(hub_articles)

    paginator = Paginator(hub_articles, 5)
    try:
        articles_paginator = paginator.page(page)
    except PageNotAnInteger:
        articles_paginator = paginator.page(1)
    except EmptyPage:
        articles_paginator = paginator.page(paginator.num_pages)

    if request.user.is_authenticated:
        notifications = notification(request)
    else:
        notifications = None

    page_data = {
        "pk": pk,
        "articles": articles_paginator,
        "last_articles": last_articles,
        "notifications": notifications,

    }
    return render(request, "articles/articles_hub.html", page_data)


def article(request, pk=None):
    hub_articles = Article.get_articles()
    last_articles = Article.get_last_articles(hub_articles)
    current_article = get_object_or_404(Article, id=pk)
    current_comments = Comment.get_comments(pk)
    notifications = notification(request)
    comments = create_comments_tree(
        current_comments, request.user if request.user.is_authenticated else None
    )
    form_comment = CommentCreateForm(request.POST or None)
    if request.user.is_authenticated:
        current_article.views.add(request.user)
        current_article.liked = current_article.likes.filter(
            pk=request.user.pk
        ).exists()
        current_article.disliked = current_article.dislikes.filter(
            pk=request.user.pk
        ).exists()
        current_article.bookmarked = current_article.bookmarks.filter(
            pk=request.user.pk
        ).exists()
        current_article.author_liked = (
            current_article.author.habruserprofile.karma_positive.filter(
                pk=request.user.pk
            ).exists()
        )
        current_article.author_disliked = (
            current_article.author.habruserprofile.karma_negative.filter(
                pk=request.user.pk
            ).exists()
        )
    page_data = {
        "article": current_article,
        "last_articles": last_articles,
        "comments": comments,
        "form_comment": form_comment,
        "media_url": settings.MEDIA_URL,
        "notifications": notifications
    }
    return render(request, "articles/article.html", page_data)


def change_article_rate(request):
    if request.is_ajax() and request.user.is_authenticated:
        rated_article = request.GET.get("article")
        field = request.GET.get("field")
        rated_article = Article.objects.get(pk=rated_article)
        if request.user != rated_article.author:
            if field == "like":
                if rated_article.likes.filter(pk=request.user.pk).exists():
                    rated_article.likes.remove(request.user)
                    rated_article.author.habruserprofile.rating -= 1
                elif rated_article.dislikes.filter(pk=request.user.pk).exists():
                    rated_article.likes.add(request.user)
                    rated_article.dislikes.remove(request.user)
                    rated_article.author.habruserprofile.rating += 2
                else:
                    rated_article.likes.add(request.user)
                    rated_article.author.habruserprofile.rating += 1
            elif field == "dislike":
                if rated_article.dislikes.filter(pk=request.user.pk).exists():
                    rated_article.dislikes.remove(request.user)
                    rated_article.author.habruserprofile.rating += 1
                elif rated_article.likes.filter(pk=request.user.pk).exists():
                    rated_article.dislikes.add(request.user)
                    rated_article.likes.remove(request.user)
                    rated_article.author.habruserprofile.rating -= 2
                else:
                    rated_article.dislikes.add(request.user)
                    rated_article.author.habruserprofile.rating -= 1
            else:
                if rated_article.bookmarks.filter(pk=request.user.pk).exists():
                    rated_article.bookmarks.remove(request.user)
                else:
                    rated_article.bookmarks.add(request.user)
            rated_article.rating = rated_article.likes.count() - rated_article.dislikes.count()
            rated_article.author.habruserprofile.save()
            rated_article.save()
        return JsonResponse(
            {
                "likes": rated_article.likes.count(),
                "dislikes": rated_article.dislikes.count(),
                "author_rating": rated_article.author.habruserprofile.rating,
                "like": rated_article.likes.filter(pk=request.user.pk).exists(),
                "dislike": rated_article.dislikes.filter(
                    pk=request.user.pk
                ).exists(),
            }
        )


def like_dislike_author_ajax(request):
    if request.is_ajax() and request.user.is_authenticated:
        user = request.GET.get("user")
        field = request.GET.get("field")
        if request.user.pk != int(user):
            user = HabrUserProfile.objects.get(pk=user)
            if field == "like":
                if user.karma_positive.filter(pk=request.user.pk).exists():
                    user.karma_positive.remove(request.user)
                elif user.karma_negative.filter(pk=request.user.pk).exists():
                    user.karma_positive.add(request.user)
                    user.karma_negative.remove(request.user)
                else:
                    user.karma_positive.add(request.user)
            elif field == "dislike":
                if user.karma_negative.filter(pk=request.user.pk).exists():
                    user.karma_negative.remove(request.user)
                elif user.karma_positive.filter(pk=request.user.pk).exists():
                    user.karma_negative.add(request.user)
                    user.karma_positive.remove(request.user)
                else:
                    user.karma_negative.add(request.user)
        user.save()
        return JsonResponse(
            {
                "karma": user.karma,
                "liked": user.karma_positive.filter(
                    pk=request.user.pk
                ).exists(),
                "disliked": user.karma_negative.filter(
                    pk=request.user.pk
                ).exists(),
            }
        )


def show_author_profile(request, pk=None):
    title = "Информация об авторе"
    author = get_object_or_404(HabrUser, pk=pk)
    author_banned_query = BannedUser.objects.filter(offender=author, is_active=True)
    if author_banned_query:
        author_banned = author_banned_query[0]
    else:
        author_banned = None
    page_data = {
        "title": title,
        "current_user": author,
        "author_banned": author_banned,
    }
    return render(request, "articles/author_profile.html", page_data)


def search_articles(request, page=1, search_query=None):
    """рендер главной страницы после поиска"""
    title = "главная страница"

    search_query = request.GET.get('search', '')
    if search_query:
        hub_articles = Article.get_search_articles(search_query)
    else:
        hub_articles = Article.get_articles()

    last_articles = Article.get_last_articles(hub_articles)
    paginator = Paginator(hub_articles, 20)
    try:
        articles_paginator = paginator.page(page)
    except PageNotAnInteger:
        articles_paginator = paginator.page(1)
    except EmptyPage:
        articles_paginator = paginator.page(paginator.num_pages)
    page_data = {
        "title": title,
        "last_articles": last_articles,
        "current_user": request.user,
        "articles": articles_paginator,
        "value_search": search_query,
    }
    return render(request, "articles/search_articles.html", page_data)


def post_list(request, pk=None, page=1):
    '''функция используется для сортировке всех статей или сортировки статей по хабу'''
    if request.is_ajax():
        sorted_query = request.GET['sorted']
        if pk is None:
            hub_articles = Sorted.sort(sorted_query).get_data()
        else:
            hub_articles = Sorted.sort(sorted_query, pk).get_data()

        paginator = Paginator(hub_articles, 5)
        try:
            articles_paginator = paginator.page(page)
        except PageNotAnInteger:
            articles_paginator = paginator.page(1)
        except EmptyPage:
            articles_paginator = paginator.page(paginator.num_pages)

        page_data = {
            "articles": articles_paginator,
            "current_user": request.user,
        }
        result = render_to_string('articles/includes/post_list.html', page_data)
        return JsonResponse({'result': result})


def post_list_search(request, page=1):
    """ функция используется для сортировке статей поиска"""
    if request.is_ajax():
        search_query = request.GET['search_value']
        sorted_query = request.GET['content']
        hub_articles = Article.get_search_articles(search_query)
        hub_articles = Sorted.sort(sorted_query, search_query=hub_articles).get_data()

        paginator = Paginator(hub_articles, 5)
        try:
            articles_paginator = paginator.page(page)
        except PageNotAnInteger:
            articles_paginator = paginator.page(1)
        except EmptyPage:
            articles_paginator = paginator.page(paginator.num_pages)

        page_data = {
            "articles": articles_paginator,
            "current_user": request.user,
            "value_search": search_query,
        }
        result = render_to_string('articles/includes/post_list.html', page_data)
        return JsonResponse({'result': result})


def post_list_user(request, user_pk, page=1):
    """ функция используется для сортировке статей пользователя"""
    if request.is_ajax():
        sorted_query = request.GET['sorted']
        if user_pk is None:
            hub_articles = Sorted.sort(sorted_query).get_data()
        else:
            hub_articles = Sorted.sort(sorted_query, user_pk).get_data()

        paginator = Paginator(hub_articles, 5)
        try:
            articles_paginator = paginator.page(page)
        except PageNotAnInteger:
            articles_paginator = paginator.page(1)
        except EmptyPage:
            articles_paginator = paginator.page(paginator.num_pages)

        page_data = {
            "articles": articles_paginator,
            "current_user": request.user,
        }
        result = render_to_string('articles/includes/post_list.html',
                                  page_data)
        return JsonResponse({'result': result})


def notification(request):
    current_notifications = []
    current_articles = Article.get_by_author(author_pk=request.user.pk)
    for itm_article in current_articles:
        likes = LikesViewed.objects.filter(article_id=itm_article.id,
                                           viewed=False)
        dislikes = DislikesViewed.objects.filter(article_id=itm_article.id,
                                                 viewed=False)
        comments = Comment.get_comments(itm_article.id) \
            .filter(viewed=False).exclude(author_id=request.user.pk)
        answered_you = Comment.get_comments(itm_article.id) \
            .filter(viewed=False,
                    parent__author_id=request.user.pk,
                    )

        likes_karma = KarmaPositiveViewed.objects.filter(
            viewed=False,
            profile_author=request.user.pk
        )
        dislikes_karma = KarmaNegativeViewed.objects.filter(
            viewed=False,
            profile_author=request.user.pk
        )

        for answer in answered_you:
            current_notifications.append(("answered_you", answer))
        for comment in comments:
            current_notifications.append(("comment", comment))
        for like in likes:
            current_notifications.append(("like", like))
        for dislike in dislikes:
            current_notifications.append(("dislike", dislike))
        for like_karma in likes_karma:
            current_notifications.append(("like_karma", like_karma))
        for dislike_karma in dislikes_karma:
            current_notifications.append(("dislike_karma", dislike_karma))
    return current_notifications


def mark_all_as_viewed(request):
    """отмечаем все уведомления как просмотренные"""
    current_articles = Article.get_by_author(author_pk=request.user.pk)
    for i in current_articles:
        LikesViewed.objects.filter(article_id=i.id).update(viewed=True)
        DislikesViewed.objects.filter(article_id=i.id).update(viewed=True)
        Comment.get_comments(i.id).update(viewed=True)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def target_mark_as_viewed(request, target, pk):
    if target == 'comment':
        Comment.objects.filter(id=pk).update(viewed=True)
    elif target == 'answered_you':
        Comment.objects.filter(id=pk).update(viewed=True)
    elif target == 'like':
        LikesViewed.objects.filter(id=pk).update(viewed=True)
    elif target == 'dislike':
        DislikesViewed.objects.filter(id=pk).update(viewed=True)
    elif target == 'like_karma':
        KarmaPositiveViewed.objects.filter(id=pk).update(viewed=True)
    elif target == 'dislike_karma':
        KarmaNegativeViewed.objects.filter(id=pk).update(viewed=True)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
