from django.shortcuts import render
import markdown
import article



# Create your views here.
from .models import Article



def main(request):
    articles = Article.objects.all()

    ctx = {}
    ctx["articles"] = articles

    return render(request, 'article/article_main.html', ctx)


def view_article(request, id):
    article = Article.objects.get(id=id)
    article.body = markdown.markdown(article.body,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ]
    )
    ctx = {}
    ctx['article'] = article

    return render(request, 'article/article_detail.html', ctx)