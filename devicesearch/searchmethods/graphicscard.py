from .clientbase import ClientBase

class GBSearch(ClientBase):
    def __init__(self):
        super().__init__()
    
    def sepOpenDirect(self,appname:str):
        self.connection()
        retlist = list()
        com = '''
            select require_item from app_sys_require_gra 
            where app_sys_require_gra.appname= ?
        '''
        print(com)
        try:
            self.cur.execute(com,[appname,])
            rows =self.cur.fetchall()
            # 1列目だけ得る
            retlist = [row[0] for row in rows]
            print(retlist)
            return retlist
        except Exception as e:
            print("GBSearch.sepOpenDirect \n" + str(e))
    
    def allValueinApp(self,appnames:list):
        self.connection()
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
            print("return_list")
            print(return_list)
            return return_list
        except Exception as e:
            print(e)
    
    def _searchover(self,vlist:list):
        append_querys = list()
        print("vlist")
        print(vlist)
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
        print("app query ")
        print(append_querys)
        return append_querys

    def maxDirectX(self,directxlist):
        self.connection()
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

    def searchover(self,exist:list,appname:str):
        #関数の辞書化
        funcdict = {
            "opengl":self.getOpenGLGraph,
            "directx":self.getDirectXGraph,
            "nvidia":self.getNVENC,
        }
        append_querys = list()
        if "opengl" in exist:
            append_querys.append(funcdict["opengl"](appname))
        elif "directx" in exist:
            append_querys.append(funcdict["directx"](appname))
        elif "nvidia" in exist:
            append_querys.append(funcdict["nvidia"](appname))
        
        return append_querys
    
    def getAppValue(self,valuetype:str,appname:str):
        self.connection()
        com = '''
            select app_sys_require_gra.require_value from app_sys_require_gra
            where require_item = ? and appname = ?
            '''
        try:
            self.cur.execute(com,(valuetype,appname,))
            rows = self.cur.fetchall()
            value = rows[0][0]
            return value
        except Exception as e:
            print(e)

    def getDirectXGraph(self,appname:str):
        value = self.getAppValue(valuetype="directx",appname=appname)
        directxcom = self.overDirectX([value])
        return directxcom

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
        
    def getOpenGLGraph(self,appname:str):
        value = self.getAppValue(valuetype="opengl",appname=appname)
        openglcom = self.overOpenGL([value])
        return openglcom

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
    
    def getLowprofile(self):
        where = '''
        graphicsboard.lowprofile = 1
        '''
        return {
            "attach":"",
            "where":where,
            "value":[]
        }
    
    def getNVENC(self,appname:str):
        value = self.getAppValue(valuetype="nvenc",appname=appname)
        nvenccom = self.overNVENC([value])
        return nvenccom
    
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

    def exe(self,com:str,value:list):
        self.connection()
        print("last")
        print(com)
        print(value)
        try:
            self.cur.execute(com,value)
            rows = self.cur.fetchall()
            return rows
        except Exception as e:
            print(e)
