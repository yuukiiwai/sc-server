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
        approws = gbs.searchover(sepres,appname)
        graboslist = list()
        for approw in approws:
            #graboELlist = list()
            grabodict = {
                "name":approw[0],
                "url":approw[1],
                "manufacture":approw[2],
                "interface":approw[3],
                "gpu":approw[7],
                "directx":approw[9],
                "opengl":approw[10],
                "lowprofile": True if approw[-1] == 1 else False
            }
            #for col in approw:
            #    graboELlist.append(col)
            graboslist.append(grabodict.copy())
            #graboslist.append(graboELlist.copy())
        
        cpuname = request.GET.get('cpu')
        if cpuname != None:
            # CPU名があれば
            cpugrrows = gbs.getmatchCPU(cpuname)
            cpugrset = set()
            for gr in cpugrrows:
                cpugrset.add(gr[0])
            
            removelist = list()
            for grabo in graboslist:
                if grabo["name"] in cpugrset:
                    pass
                else:
                    removelist.append(grabo)
            
            for grabo in removelist:
                graboslist.remove(grabo)
        
        lowprofile = request.GET.get('lowprofile')
        if lowprofile != None:
            #ロープロファイルチェックが有れば
            removelist = list()
            for grabo in graboslist:
                if not grabo["lowprofile"]:
                    removelist.append(grabo)
            
            for grabo in removelist:
                graboslist.remove(grabo)

        context = {
            "gra_list":graboslist
        }
        return Response(context,status.HTTP_200_OK)