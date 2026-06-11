from django.shortcuts import render

def base(request):
    return render(request, 'base.html')

def index(request):
    return render(request, 'index.html')

def admin(request):
    return render (request,)

from django.shortcuts import render

def index(request):
    print(">>> VIEW INDEX CHAMADA <<<")
    return render(request, 'index.html')