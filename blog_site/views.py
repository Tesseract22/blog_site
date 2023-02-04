from django.shortcuts import render, redirect
# from article.models import Article



def main_site(request):

    return render(request, "chat.html")

def test(request):

    return render(request, "test.html")