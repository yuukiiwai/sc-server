from django.shortcuts import render

def robots(request):
    return render(request,'static/robots.txt')