from .clientbase import ClientBase

class GBSearch(ClientBase):
    def __init__(self):
        super().__init__()
    
    def sepOpenDirect(self,appname:str):
        apinum = 2
        params = list()
        for i in range(apinum):
            params.append(appname)
        self.connection()
        com = f'''
            select exists (
            select require_item from app_sys_require 
            where app_sys_require.appname= ?
            and require_item="opengl"
            ) as openglcheckexists, 
            ( select require_item from app_sys_require 
            where app_sys_require.appname = ?
            and require_item="directx") as directxcheck
        '''
        try:
            self.cur.execute(com,params)
            rows =self.cur.fetchall()
            return rows[0]
        except Exception as e:
            print("GBSearch.sepOpenDirect \n" + str(e))
    
    def overDirectX(self,versions:list):
        self.connection()
        fmt = ','.join(['?'] * len(versions))

        com = '''
        select * from graphicsboard
        join directxrank
        on graphicsboard.directx = directxrank.directx_version
        where directxrank.ranknum >=
        (select max(directxrank.ranknum) from directxrank
        where directxrank.directx_version in (%s)
        )
        ''' % fmt
        try:
            self.cur.execute(com,versions)
            rows = self.cur.fetchall()
            return rows
        except Exception as e:
            print("GBSearch.overDirectX \n" + str(e))
    
    def overOpenGL(self,versions:list):
        self.connection()
        declist = list()
        max = 0
        for version in versions:
            declist.append(float(version))
        for dec in declist:
            if max < dec:
                max = dec
        
        com = f'''
        select * from graphicsboard
        where graphicsboard.opengl >= {max}
        '''
        try:
            self.cur.execute(com)
            rows = self.cur.fetchall()
            return rows
        except Exception as e:
            print("GBSearch.overOpenGL \n" + str(e))
    
    def searchover(self,exist:set(),appname:str):
        #関数の辞書化
        funcdict = {
            0:self.getOpenGLGraph,
            1:self.overDirectX,
        }
        i = 0
        resultover = dict()
        for col in exist:
            if col == 1:
                resultover = funcdict[i](appname)
            i += 1
        return resultover
    
    def getOpenGLValue(self,appname:str):
        self.connection()
        com = '''
            select app_sys_require.require_value from app_sys_require
            where require_item = "opengl" and appname = ?
            '''
        try:
            self.cur.execute(com,(appname,))
            rows = self.cur.fetchall()
            value = rows[0][0]
            return value
        except Exception as e:
            print(e)
    
    def getOpenGLGraph(self,appname:str):
        value = self.getOpenGLValue(appname)
        rows = self.overOpenGL([value])
        return rows

    def getmatchCPU(self,cpu:str):
        
        com = '''
        select graphicsboard.graphicsboard_name
        from graphicsboard
        join cpu
        on graphicsboard.interface_gen = cpu.PCIe_gen AND graphicsboard.interface_prot = cpu.PCIe_prot_best
        where cpu.name = ?
        group by graphicsboard.graphicsboard_name;
        '''
        self.connection()
        try:
            self.cur.execute(com,(cpu,))
            rows = self.cur.fetchall()
            return rows
        except Exception as e:
            print(e)
