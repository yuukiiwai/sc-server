import string
from .clientbase import ClientBase


class AllSearch(ClientBase):
    def __init__(self):
        super().__init__()
    
    def all_gra(self):
        com = 'select graphicsboard_name from graphicsboard;'
        value = self.valueSelect(com)
        return value


    def all_app(self):
        # !!! only gra !!! have to check!
        com = 'select distinct appname from app_sys_require_gra;'
        value = self.valueSelect(com)
        return value
    
    def valueSelect(self,com:string):
        self.connection()
        try:
            self.cur.execute(com)
            rows = self.cur.fetchall()
            value = [ row[0] for row in rows]
            self.conClose()
            return value
        except Exception as e:
            print(e)
            self.conClose()
            return None
