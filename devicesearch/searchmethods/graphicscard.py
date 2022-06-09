from clientbase import ClientBase

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
        );
        '''
        try:
            self.cur.execute(com)
            rows = self.cur.fetchall()
            return rows
        except Exception as e:
            print("GBSearch.overDirectX \n" + str(e))
    