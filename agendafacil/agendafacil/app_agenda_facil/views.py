from django.shortcuts import render

def base(request):
    return render(request, 'base.html')


def admin(request):
    return render (request,)