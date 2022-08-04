from django.shortcuts import render




def main_site(request):

    return render(request, "main.html")

def test(request):

    return render(request, "test.html")