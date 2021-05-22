from ckeditor_uploader.views import upload
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include

urlpatterns = [
    path("", include("apps.articles.urls", namespace="articles")),
    path("account/", include("apps.account.urls", namespace="account")),
    path("auth/", include("apps.authorization.urls", namespace="auth")),
    path("admin/", admin.site.urls, name="admin"),
    path("comments/", include("apps.comments.urls", namespace="comments")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("upload/", login_required(upload), name="ckeditor_upload"),
    path("", include("social_django.urls", namespace="social")),
    path("moderator/", include("apps.moderator.urls", namespace="moderator")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# http://127.0.0.1:8000/complete/vk-oauth2/
# https://www.sputnik-seven.xyz/complete/vk-oauth2/
# http://localhost:8000/complete/vk-oauth2/
# https://coderoad.ru/54375834/%D0%97%D0%B0%D0%BF%D1%83%D1%81%D1%82%D0%B8%D1%82%D0%B5-%D0%BD%D0%B5%D1%81%D0%BA%D0%BE%D0%BB%D1%8C%D0%BA%D0%BE-%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%BE%D0%B2-django-%D1%81-nginx-%D0%B8-gunicorn