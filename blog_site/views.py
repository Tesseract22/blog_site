from django.shortcuts import render, redirect
# from article.models import Article



def main_site(request):

    return redirect('article:list')

def test(request):

    return render(request, "test.html")