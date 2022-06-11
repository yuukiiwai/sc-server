import MySQLdb
from SatisfactionConfiguration import secret

class ClientBase():
    def connection(self):
        self.conn = MySQLdb.connect(
            user=secret.DB_USER,
            passwd=secret.DB_PASS,
            host='localhost',
            db=secret.DB_DBNAME,
            use_unicode=True,
            charset="utf8"
        )
        self.cur = self.conn.cursor()

    def conClose(self):
        self.cur.close()
        self.conn.close()
    
    def commitAclose(self):
        self.conn.commit()
        self.conClose()