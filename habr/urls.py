from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("apps.articles.urls", namespace="articles")),
    path("account/", include("apps.account.urls", namespace="account")),
    path("auth/", include("apps.authorization.urls", namespace="auth")),
    path("admin/", admin.site.urls),
    path(r'^ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
