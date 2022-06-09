from .clientbase import ClientBase

class GBSearch(ClientBase):
    def __init__(self):
        pass
    
    def overDirectX(self,versions:list):
        self.connection()
        inq = ""
        for version in versions:
            inq = inq + f'"{version}",'
        inq = inq[:-1]

        com = f'''
        select * from graphicsboard
        join directxrank
        on graphicsboard.directx = directxrank.directx_version
        where directxrank.ranknum >=
        (select max(directxrank.ranknum) from directxrank
        where directxrank.directx_version in ({inq})
        )
        '''
        try:
            self.cur.execute(com)
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
    
    def sepOpenDirect(self,appname:str):
        apinum = 2
        params = list()
        for i in range(apinum + 1):
            params.append(appname)
        self.connection()
        com = f'''
            select exists (
            select require_item from app_sys_require 
            where app_sys_require.appname="{appname}"
            and require_item="opengl"
            ) as openglcheckexists, 
            ( select require_item from app_sys_require 
            where app_sys_require.appname ="{appname}" 
            and require_item="directx") as directxcheck
        '''
        try:
            self.cur.execute(com)
            rows =self.cur.fetchall()
            return rows[0]
        except Exception as e:
            print("GBSearch.sepOpenDirect \n" + str(e))
    
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
        com = f'''
            select app_sys_require.require_value from app_sys_require
            where require_item = "opengl" and appname = "{appname}"
            '''
        try:
            self.cur.execute(com)
            rows = self.cur.fetchall()
            value = rows[0][0]
            return value
        except Exception as e:
            print(e)
    
    def getOpenGLGraph(self,appname:str):
        value = self.getOpenGLValue(appname)
        rows = self.overOpenGL([value])
        return rows
