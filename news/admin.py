from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Article


class ArticleAdmin(SummernoteModelAdmin):
    exclude = ('author',)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(ArticleAdmin, self).save_model(request, obj, form, change)


admin.site.register(Article, ArticleAdmin)
