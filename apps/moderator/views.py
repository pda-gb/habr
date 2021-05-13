from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.timezone import now
from apps.articles.models import Article
from datetime import datetime
from apps.moderator.forms import BannedUserForm
from apps.moderator.models import VerifyArticle, BannedUser
from apps.authorization.models import HabrUser
from apps.moderator.forms import BannedUserForm, RemarkCreateForm
from apps.moderator.models import BannedUser, VerifyArticle


def complaints(request):
    title = "Жалобы"
    page_data = {
        'title': title,
    }
    return render(request, "moderator/complaints.html", page_data)


def review_articles(request):
    """получение всех статей на проверку"""
    articles = VerifyArticle.get_all_articles_for_verifications()
    title = "Статьи на проверку"
    page_data = {
        "title": title,
        "articles": articles,
    }
    return render(request, "moderator/review_articles.html", page_data)


def add_user_ban(request, pk):
    title = "Блокирование пользователя"
    current_user = HabrUser.objects.get(pk=pk)

    if request.method == 'POST':
        ban_form = BannedUserForm(request.POST)
        if ban_form.is_valid():
            banned_user_query = BannedUser.objects.filter(offender=pk)
            if banned_user_query:
                banned_user = banned_user_query[0]
                banned_user.is_active = True
                banned_user.reason = request.POST["reason"]
                if request.POST.get("is_forever"):
                    banned_user.is_forever = True
                else:
                    banned_user.is_forever = False
                banned_user.num_days = request.POST["num_days"]
                banned_user.date_ban = datetime.today()
                banned_user.save()
            else:
                banned_user = BannedUser.objects.create(offender=current_user,
                                          reason=request.POST["reason"],
                                          num_days=request.POST["num_days"],
                                          is_active=True,
                                          is_forever=True if request.POST.get("is_forever") else False)
            banned_user.set_ban_email()
            return HttpResponseRedirect(reverse("articles:author_profile", args=[pk]))
        else:
            messages.error(request, 'ошибка')
    else:
        ban_form = BannedUserForm()
    page_data = {
        "title": title,
        "ban_form": ban_form,
        "current_user_pk": pk,
    }
    return render(request, 'moderator/add_ban.html', page_data)


def remove_user_ban(request, pk):
    current_user = BannedUser.objects.get(offender=pk)
    current_user.delete()
    current_user.unset_ban_email()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# def remove_user_ban(request, pk):
#     if request.is_ajax():
#         current_user = BannedUser.objects.get(offender=pk)
#         current_user.delete()
#         content = {
#             'current_user': current_user,
#             'user': request.user,
#         }
#         # result = render_to_string('moderator/includes/ban_buttons.html', content)
#         result = render_to_string('articles/author_profile.html', content)
#         return JsonResponse({'result': result})


def banned_users(request):
    title = "Заблокированные пользователи"
    banned_users_query = BannedUser.objects.filter(is_active=True)
    page_data = {
        "title": title,
        "banned_users": banned_users_query
    }
    return render(request, "moderator/banned_users.html", page_data)


def allow_publishing(request, pk):
    """Разрешение модератором публикации статьи"""
    VerifyArticle.objects.filter(verification=pk).update(is_verified=True)
    Article.objects.filter(id=pk).update(draft=False)
    Article.objects.filter(id=pk).update(published=now(), updated=now())
    return HttpResponseRedirect(reverse('moderator:review_articles'))


def reject_publishing(request, pk):
    """Отказ модератором на публикацию статьи"""
    form_remark = RemarkCreateForm(request.POST or None)
    page_data = {
        "pk": pk,
        "form_remark": form_remark,
    }
    return render(request, 'moderator/form_return_article.html', page_data)


def return_article(request, pk):
    """отправка на доработку и с обязательной причиной отказа"""
    if request.method == 'POST':
        form_remark = RemarkCreateForm(request.POST or None)
        if form_remark.is_valid():
            VerifyArticle.objects.filter(verification=pk).update(
                is_verified=False,
                remark=request.POST["remark"]
            )
            Article.objects.filter(id=pk).update(updated=now())

    else:
        form_remark = RemarkCreateForm()
    return HttpResponseRedirect(reverse("moderator:review_articles"))
