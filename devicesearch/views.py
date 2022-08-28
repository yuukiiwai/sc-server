from email import message
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

def gbpackaging(rows):
    grabolist = list()
    for row in rows:
        grabodict = {
            "id":row[0],
            "name":row[1],
            "url":row[2],
            "manufacture":row[3],
            "interface":row[4],
            "gpu":row[5],
            "directx":row[6],
            "opengl":row[7],
            "lowprofile": True if row[8] == 1 else False,
            "img_url":row[9]
            }
        grabolist.append(grabodict)
    return grabolist

class getAppSat_Gra(APIView):
    def get(self,request,format=None):
        appnames = request.GET.getlist('appname[]')
        if appnames == None:
            return Response(status=status.HTTP_200_OK)
        gbs = GBSearch()
        req_item_ = gbs.allValueinApp(appnames = appnames)
        grabo_que_list_ = gbs._searchover(req_item_)
        com = '''select graphicsboard.id,
        graphicsboard.graphicsboard_name,
        graphicsboard.url,
        graphicsboard.manufacture,
        graphicsboard.interface,
        graphicsboard.gpu,
        graphicsboard.directx,
        graphicsboard.opengl,
        graphicsboard.lowprofile,
        graphicsboard.image_url
        from graphicsboard '''
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
        
        # ↓ returnする値入れ
        grabolist = list()
        if where != "where 1 = 1 ":
            rows = gbs.exe(com=com+where,value=paralist)
            if rows == None:
                return Response({"message":"Sorry unskilled"},status.HTTP_200_OK)
            grabolist = gbpackaging(rows=rows)
        else:
            print("app")
            return Response({"message":"Sorry Non App"},status.HTTP_200_OK)

        if len(grabolist) == 0:
            return Response({"message":"Sorry Non Card"},status.HTTP_200_OK)
        
        context = {
            "message" : "Thank",
            "gra_list":grabolist
        }

        gbs.end()

        return Response(context,status.HTTP_200_OK)

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
            "g1":" select id,graphicsboard_name,url,manufacture,interface,gpu,directx,opengl,lowprofile,image_url from graphicsboard join nvidia_gpu on nvidia_gpu.gpu_name = graphicsboard.gpu order by nvidia_gpu.nvidia_rank desc limit 20",
            "g2":" select id,graphicsboard_name,url,manufacture,interface,gpu,directx,opengl,lowprofile,image_url from graphicsboard where opengl >= 4.5 order by opengl desc limit 20"
        }
    def get(self,request,format=None):
        rtype = request.GET.get("t")
        rmode = request.GET.get("r")
        sql = self.rdic[rtype+rmode]
        gbs = GBSearch()
        rows = gbs.exe(sql,[])
        gblist = gbpackaging(rows=rows)
        context = {
            "gra_list":gblist
        }
        print(gblist)
        gbs.end()
        return Response(context,status.HTTP_200_OK)

class getGra(APIView):
    def get(self,request,id,format=None):
        gbs = GBSearch()
        row = gbs.getDetail(id=id)
        # 存在しないidを要求されたら404
        if row == None:
            return Response({
                "message":"sorry",
            },status.HTTP_404_NOT_FOUND)
        grainfo = {
            "id":id,
            "name":row[0],
            "url":row[1],
            "manufacture":row[2],
            "interface":row[3],
            "interface_gen":row[4],
            "interface_shape":row[5],
            "interface_prot":row[6],
            "gpu":row[7],
            "gpu_manufacture":row[8],
            "directx":row[9],
            "opengl":row[10],
            "lowprofile": True if row[11] == 1 else False,
            "img_url":row[12]
        }
        context = {
            "message":"thankyou",
            "gra_info":grainfo
        }
        print(context)
        gbs.end()
        return Response(context,status.HTTP_200_OK)