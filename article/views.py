from django.shortcuts import render



# Create your views here.
from .models import Article


def article_main(request):
    return render(request, "article_main.html")

def view_articles(request):
    articles = Article.objects.all()

    ctx = {}
    ctx["articles"] = articles

    return render(request, 'article/article_main.html', ctx)