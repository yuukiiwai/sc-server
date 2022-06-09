from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .searchmethods.graphicscard import GBSearch

# Create your views here.
def top(request):
    return render(request,'devicesearch/top.html')

class getAppSat_Gra(APIView):

    def get(self,request,format=None):
        appname = request.GET.get('appname')
        if appname == None:
            return Response(status=status.HTTP_200_OK)
        
        gbs = GBSearch()
        sepres = gbs.sepOpenDirect(appname=appname)
        rows = gbs.searchover(sepres,appname)
        graboslist = list()
        for row in rows:
            graboELlist = list()
            grabodict = {
                "name":row[0],
                "url":row[1],
            }
            for col in row:
                graboELlist.append(col)
            graboslist.append(grabodict.copy())
            #graboslist.append(graboELlist.copy())
        context = {
            "gra_list":graboslist
        }
        return Response(context,status.HTTP_200_OK)