from django.shortcuts import render

# Create your views here.



def calculator_main(request):
    return render(request, "calculator/calculator_main.html")


def factorio(request):
    
    return render(request, "calculator/calculator_main.html") 