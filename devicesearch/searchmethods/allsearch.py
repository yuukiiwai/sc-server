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
        com = 'select distinct appname from app_sys_require;'
        value = self.valueSelect(com)
        return value
    
    def valueSelect(self,com:string):
        self.connection()
        try:
            self.cur.execute(com)
            rows = self.cur.fetchall()
            value = [ row[0] for row in rows]
            return value
        except Exception as e:
            print(e)
            return None