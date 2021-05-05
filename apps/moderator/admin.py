from django.contrib import admin
from .models import Moderator, BannedUser, BannedComment, VerifyArticle

admin.site.register(Moderator)
admin.site.register(BannedUser)
admin.site.register(BannedComment)
admin.site.register(VerifyArticle)

