from SatisfactionConfiguration import secret
import mysql.connector as mcon

class ClientBase():
    def __init__(self):
        self.config = {
            'user':secret.DB_USER,
            'passwd':secret.DB_PASS,
            'host':secret.DB_HOST,
            'db':secret.DB_DBNAME,
        }
    def connection(self):
        self.cnx = mcon.connect(**self.config)
        self.cur = self.cnx.cursor(prepared=True)

    def conClose(self):
        self.cur.close()
        self.cnx.close()
    
    def commitAclose(self):
        self.cnx.commit()
        self.conClose() 