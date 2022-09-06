from django.contrib import admin

from .forms import AlbumForm
from .models import Article

@admin.register(Article)
class ArticleModelAdmin(admin.ModelAdmin):
    form = AlbumForm
    fields = [
        'title',
        'body',
        'author',
        ]