import psycopg2

class MyPostgresqlOp():
    conn=None

    _database=""
    _user=""
    _password=''
    _host=''
    _port=''
    def __init__(self):
        pass
    def __del__(self):
        try:
            if(self.conn!=None):
                self.conn.close()
        except Exception as ex:
            pass
        ''''
        我们在PG数据库，关闭了事务的自动提交的情况下，会经常的遇到这样的问题
    ERROR:  current transaction is aborted, commands ignored until end of transaction block
    这个时候，由于这不操作错误了，那么后面所有的这个会话中的操作都会报
    这个时候，我们要解决这个问题，只能够使用rollback，或者是commit去解决
        '''
    def clearException(self):
        self.conn.commit()
    def _chk_connect(self):
        if self.conn==None:
            self.connect(self._database,self._user,self._password,self._host,self._port)
    def setConnectParams(self,database,user,password,host,port):
        self._database=database
        self._user=user
        self._password=password
        self._host=host
        self._port=port
    def connect(self,database,user,password,host,port):
        self.conn=psycopg2.connect(database=database,user=user,password=password,host=host,port=port)
        return self.conn
    def select(self,sql):
        self._chk_connect()
        cur=self.conn.cursor()
        row=cur.execute(sql)
        #rows=cur.fetchall()
        coloumns = [row[0] for row in cur.description]
        result = [[str(item) for item in row] for row in cur.fetchall()]
        cur.close()
        return [dict(zip(coloumns, row)) for row in result]

    def execNoQuery(self,sql)->int:
        self._chk_connect()
        cur = self.conn.cursor()
        cur.execute(sql)
        count=cur.rowcount
        self.conn.commit()
        cur.close()
        return count
if(__name__=='__main__'):
    pg=MyPostgresqlOp()
    pg.connect("zhaoyuan","postgres","sql510115","127.0.0.1",5432)
    count=pg.execNoQuery("insert into test1 (f1,f2) values(0.1,0.2)")
    print(count)
