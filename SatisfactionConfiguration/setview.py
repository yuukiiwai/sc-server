from django.shortcuts import render,redirect

def robots(request):
    return render(request=request,template_name='robots.txt',content_type='text/plain')

def sslaccept(request):
    return render(request=request,template_name='236f9aea9d639cee6a61b04b04c6d1b5.txt',content_type='text/plain')

def home(request):
    return render(request=request,template_name='index.html')