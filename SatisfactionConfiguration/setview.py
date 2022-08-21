from django.shortcuts import render

def robots(request):
    return render(request=request,template_name='robots.txt',content_type='text/plain')