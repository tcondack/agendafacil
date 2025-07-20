from django.shortcuts import render

def base(request):
    return render(request, 'static/template/home.html')
