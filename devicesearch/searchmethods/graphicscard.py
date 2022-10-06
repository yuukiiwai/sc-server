from .clientbase import ClientBase

class GBSearch(ClientBase):
    def __init__(self):
        super().__init__()
        self.connection()
    
    def allValueinApp(self,appnames:list):
        fmt = ','.join(["?"]*len(appnames))
        com = '''
            select require_item,require_value from app_sys_require_gra
            where app_sys_require_gra.appname in (%s)
            order by require_item
        ''' % fmt
        try:
            self.cur.execute(com,appnames)
            rows = self.cur.fetchall()
            processed_name = list()
            return_list = list()
            for row in rows:
                tagname = row[0]
                if tagname in processed_name:
                    continue
                vdict_origin = {
                    "tagname":tagname,
                    "list":[]
                }
                for row2 in rows:
                    if tagname == row2[0]:
                        vdict_origin["list"].append(row2[1])
                return_list.append(vdict_origin.copy())
                processed_name.append(row[0])
            #print("return_list")
            #print(return_list)
            return return_list
        except Exception as e:
            print(e)
    
    def _searchover(self,vlist:list):
        append_querys = list()
        for v in vlist:
            if v["tagname"] == "directx":
                dxv = self.maxDirectX(v["list"])
                append_querys.append(self.overDirectX(dxv))
            elif v["tagname"] == "opengl":
                ogv = self.maxOpengl(v["list"])
                append_querys.append(self.overOpenGL(ogv))
            elif v["tagname"] == "nvenc":
                nvv = self.maxNvenc(v["list"])
                append_querys.append(self.overNVENC(nvv))
            elif v["tagnage"] == "nvidia_name":
                nvName = self.maxNvidiaName(v["list"])
                append_querys.append(self.overNvidiaName(nvName))
            elif v["tagname"] == "memory_capaG":
                memcG = self.maxMemcapa(v["list"])
                append_querys.append(self.overMemcap(memcG))
        print("app query ")
        print(append_querys)
        return append_querys

    def maxDirectX(self,directxlist):
        fmt = ','.join(["?"]*len(directxlist))
        com = '''
        select max(directxrank.ranknum) from directxrank
        where directxrank.directx_version in (%s);
        ''' % fmt
        try:
            self.cur.execute(com,directxlist)
            rows = self.cur.fetchall()
            return rows[0][0]
        except Exception as e:
            print(e)

    def maxNvenc(self,vlist:list):
        vpro = [int(v) for v in vlist]
        return max(vpro)
    
    def maxOpengl(self,vlist:list):
        vpro = [float(v) for v in vlist]
        return max(vpro)

    def maxNvidiaName(self,namelist:list):
        fmt = ','.join(["?"]*len(namelist))
        com = '''
        select max(nvidia_gpu.nvidia_rank) from nvidia_gpu
        where nvidia_gpu.gpu_name in (%s);
        ''' % fmt
        try:
            self.cur.execute(com,namelist)
            rows = self.cur.fetchall()
            return rows[0][0]
        except Exception as e:
            print(e)

    def maxMemcapa(self,clist:list):
        capa = [int(c) for c in clist]
        return max(capa)

    def overDirectX(self,version):
        attach = '''
        join directxrank
        on graphicsboard.directx = directxrank.directx_version
        ''' 
        where = '''
        directxrank.ranknum >= ?
        '''
        return{
            "attach":attach,
            "where":where,
            "value":[version]
        }
    
    def overOpenGL(self,version):
        where = '''
        graphicsboard.opengl >= ?
        '''
        retdict = {
            "attach":"",
            "where":where,
            "value":[version]
        }
        return retdict
        
    def overNvidiaName(self,version):
        attach = '''
        join nvidia_gpu
        on graphicsboard.gpu = nvidia_gpu.gpu_name
        '''
        where = '''
        nvidia_gpu.nvidia_rank >= ?
        '''
        return{
            "attach":attach,
            "where":where,
            "value":[version]
        }

    def overMemcap(self,capa):
        where = '''
        graphicsboard.memory_capaG >= ?
        '''
        return {
            "attach":"",
            "where":where,
            "value":[capa]
        }

    def getmatchCPU(self,cpu:str):
        
        attach = '''
        join cpu
        on graphicsboard.interface_gen = cpu.PCIe_gen AND graphicsboard.interface_prot = cpu.PCIe_prot_best
        '''
        where = '''
        cpu.name = ?
        '''
        return{
            "attach":attach,
            "where":where,
            "value":[cpu]
        }
    
    def overNVENC(self,version):
        attach = '''
        join nvidia_gpu 
        on nvidia_gpu.gpu_name = graphicsboard.gpu
        '''
        where = '''
        nvidia_gpu.nvenc_gen >= ?
        '''

        retdict = {
            "attach":attach,
            "where":where,
            "value":[version]
        }
        return retdict
    
    def getLowprofile(self):
        where = '''
        graphicsboard.lowprofile = 1
        '''
        return {
            "attach":"",
            "where":where,
            "value":[]
        }
    
    def exe(self,com:str,value:list):
        print("last")
        print(com)
        print(value)
        try:
            self.cur.execute(com,value)
            rows = self.cur.fetchall()
            return rows
        except Exception as e:
            print(e)

    def getDetail(self,id:int):
        com = '''
        select graphicsboard_name,url,manufacture,interface,interface_gen,interface_shape,interface_prot,gpu,gpu_manufacture,directx,opengl,lowprofile,image_url
        from graphicsboard
        where id = ?
        '''
        try:
            self.cur.execute(com,[id])
            # 1データだけが取られるはずなので、[0]指定
            rows = self.cur.fetchall()[0]
            return rows
        except Exception as e:
            print(e)

    def end(self):
        self.conClose()