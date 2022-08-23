from multiprocessing import context
from devicesearch.searchmethods.allsearch import AllSearch
from .searchmethods.allsearch import AllSearch
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
        appnames = request.GET.getlist('appname[]')
        if appnames == None:
            return Response(status=status.HTTP_200_OK)
        gbs = GBSearch()
        req_item_ = gbs.allValueinApp(appnames = appnames)
        grabo_que_list_ = gbs._searchover(req_item_)
        com = 'select * from graphicsboard '
        where = "where 1 = 1 "
        paralist=list()
        for que in grabo_que_list_:
            com += que["attach"]
            where += " and " + que["where"]
            paralist += que["value"]
        
        cpuname = request.GET.get('cpu')
        if cpuname != None:
            # CPU名があれば
            cpugrque = gbs.getmatchCPU(cpuname)
            com += cpugrque["attach"]
            where += " and " + cpugrque["where"]
            paralist += cpugrque["value"]
        
        lowprofile = request.GET.get('lowprofile')
        if lowprofile != None:
            #ロープロファイルチェックが有れば
            lowproque = gbs.getLowprofile()
            com += lowproque["attach"]
            where += " and " + lowproque["where"]
            paralist += lowproque["value"]

        if where != "where 1 = 1 ":
            rows = gbs.exe(com=com+where,value=paralist)
            grabolist = self.gbpackaging(rows=rows)
        else:
            grabolist = list()
        
        context = {
            "message" : "Sorry" if len(grabolist) == 0 else "Thank",
            "gra_list":grabolist
        }

        gbs.end()

        return Response(context,status.HTTP_200_OK)
    
    def gbpackaging(self,rows):
        grabolist = list()
        for row in rows:
            grabodict = {
                    "name":row[0],
                    "url":row[1],
                    "manufacture":row[2],
                    "interface":row[3],
                    "gpu":row[7],
                    "directx":row[9],
                    "opengl":row[10],
                    "lowprofile": True if row[-1] == 1 else False
                }
            grabolist.append(grabodict)
        return grabolist

class AllApp(APIView):
    def get(self,request,format=None):
        aps = AllSearch()
        apps = aps.all_app()
        context = {
            "apps":apps
        }
        print(context)
        return Response(context,status.HTTP_200_OK)

class AllGra(APIView):
    def get(self,request,format=None):
        grs = AllSearch()
        gras = grs.all_gra()
        context = {
            "gras":gras
        }
        return Response(context,status.HTTP_200_OK)

class Recommend(APIView):
    def __init__(self):
        super()
        self.rdic = {
            "g1":" select graphicsboard.* from graphicsboard join nvidia_gpu on nvidia_gpu.gpu_name = graphicsboard.gpu order by nvidia_gpu.nvidia_rank desc limit 20",
            "g2":" select graphicsboard.* from graphicsboard where opengl >= 4.5 order by opengl desc limit 20"
        }
    def get(self,request,format=None):
        rtype = request.GET.get("t")
        rmode = request.GET.get("r")
        sql = self.rdic[rtype+rmode]
        gbs = GBSearch()
        rows = gbs.exe(sql,[])
        gblist = getAppSat_Gra().gbpackaging(rows=rows)
        context = {
            "gra_list":gblist
        }
        gbs.end()
        return Response(context,status.HTTP_200_OK)
