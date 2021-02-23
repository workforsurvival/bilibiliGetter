import pymysql.cursors

class mysql_helper:
    def __init__(self):
        self._conn = pymysql.connect(
            #host='128.14.150.254',
            host='localhost',
            port=3306,
            user='root',
            password='jinri52',
            db='bidata',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def exec(self,query,tup):
        with self._conn.cursor() as cursor:
            cursor.execute(query,tup)
            self._conn.commit()

    def insertR(self,query,tup):
        with self._conn.cursor() as cursor:
            cursor.execute(query,tup)
            self._conn.commit()
            return cursor.lastrowid

    def updateR(self,query,tup):
        with self._conn.cursor() as cursor:
            cursor.execute(query,tup)
            self._conn.commit()
            return cursor.lastrowid

    def contentsCheckInsert(self,query,tup,cid):
        if(self.selectCount("contents",'cid',cid))==0:
            return self.insertR(query,tup)
        else:
            return self.fetchone("select contUid from contents where cid=%s",(cid))['contUid']

    def selectCount(self,table,uid,val):
        try:
            with self._conn.cursor() as cursor:
                query="select count(*) as cnt from "+table+" where "+uid+"='"+val+"'"
                cursor.execute(query)
                result = cursor.fetchone()
                return result['cnt']
        except:
            pass

    def getRecords(self,type):
        with self._conn.cursor() as cursor:
            cursor.execute("select * from comments where type=%s",(type))
            result = list(cursor.fetchall())
            return result

    def fetch(self,query):
        with self._conn.cursor() as cursor:
            cursor.execute(query)
            result = list(cursor.fetchall())
            return result
    def fetchone(self,query,tup):
        with self._conn.cursor() as cursor:
            cursor.execute(query,tup)
            result = cursor.fetchone()
            return result

    def insertConn(self,table,col1,col2,val1,val2):
        with self._conn.cursor() as cursor:
            query = "INSERT INTO "+table+" set "+col1+"="+val1+","+col2+"="+val2
            cursor.execute(query)
            self._conn.commit()
            return cursor.lastrowid
    #구글번역용 
    def getTrans(self,cTable,cField,jField):
        with self._conn.cursor() as cursor:
            cursor.execute("SELECT * from "+cTable+" where "+cField+" is null and "+jField+" is not null")
            result = list(cursor.fetchall())
            return result
