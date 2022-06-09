from django.db import connection

class ClientBase():
    def connection(self):
        self.cur = connection.cursor()

    def conClose(self):
        connection.close()
    
    def commitAclose(self):
        connection.commit()
        self.conClose()