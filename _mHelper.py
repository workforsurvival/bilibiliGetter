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

    def initCids(self,startLimit,limit):
        with self._conn.cursor() as cursor:
            query = "SELECT uid,cid from Product where is_inserted=0 order by uid asc limit %s,%s"
            tup = (startLimit,limit)
            cursor.execute(query,tup)
            result = list(cursor.fetchall())
            return result
    def initCidss(self):
        with self._conn.cursor() as cursor:
            query = "SELECT uid,cid from Product where is_inserted=0 order by uid asc"
            cursor.execute(query)
            result = list(cursor.fetchall())
            return result
    
    def initCidCount(self):
        with self._conn.cursor() as cursor:
            query="select count(*) as cnt from Product where is_inserted=0"
            cursor.execute(query)
            result = cursor.fetchone()
            return result['cnt']

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

    def ProductCheckInsert(self,query,tup,cid):
        if(self.selectCount("Product",'cid',cid))==0:
            return self.insertR(query,tup)
        else:
            return self.fetchone("select uid from Product where cid=%s",(cid))['uid']
    def ProductCheckUpdate(self,query,tup,cid):
        if(self.selectCount("Product",'cid',cid))>0:
            self.updateR(query,tup)
            return self.fetchone("select uid from Product where cid=%s",(cid))['uid']
        else:
            return null

    def mm_check_insert(self,table,cid,name):
        if(self.selectCount(table,'cid',cid))==0:
            return self.insertR("insert into "+table+" set cid=%s,ja_name=%s",(cid,name))
        else:
            return self.fetchone("select uid from "+table+" where cid=%s",(cid))['uid']
    def simg_check_insert(self,cid,img_link):
        if(self.selectCount("Simg",'img_link',img_link))==0:
            return self.insertR("insert into Simg set cid=%s,img_link=%s",(cid,img_link))
        else:
            return self.fetchone("select uid from Simg where cid=%s",(cid))['uid']
    
    def selectCount(self,table,uid,val):
        with self._conn.cursor() as cursor:
            query="select count(*) as cnt from "+table+" where "+uid+"='"+val+"'"
            cursor.execute(query)
            result = cursor.fetchone()
            return result['cnt']

    def checkMtoM(self,table_name,product_id,conn_id_name,val_id):
        with self._conn.cursor() as cursor:
            cursor.execute("select count(*) as cnt from "+table_name+" where product_id=%s and "+conn_id_name+"=%s",(product_id,val_id))
            result = cursor.fetchone()
            return result['cnt']

    def selectItemAll(self):
        with self._conn.cursor() as cursor:
            query = "select * from Item"
            cursor.execute(query)
            result = list(cursor.fetchall())
            return result

    def selectActors(self):
        with self._conn.cursor() as cursor:
            query = "select * from Actor where total_film is null;"
            cursor.execute(query)
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
    def getcateid(self,cate_name):
        with self._conn.cursor() as cursor:
            query="select cate_uid from to_category where cate_name='"+cate_name+"'"
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                return result['cate_uid']
            else:
                return 14
    def itemIsExits(self,wr_id,bo_table):
        with self._conn.cursor() as cursor:
            query="select count(*) as cnt from to_item where wr_id='"+wr_id+"' && bo_table='"+bo_table+"'"
            cursor.execute(query)
            result = cursor.fetchone()
            return result['cnt']
    def fileIsExits(self,file_name):
        with self._conn.cursor() as cursor:
            query="select count(*) as cnt from to_file where file_name='"+file_name+"'"
            cursor.execute(query)
            result = cursor.fetchone()
            return result['cnt']
    # def getclassid(self,class_name):
    #     with self._conn.cursor() as cursor:
    #         query="select class_uid from to_class where class_name='"+class_name+"'"
    #         cursor.execute(query,tup)
    #         result = cursor.fetchone()
    #         return result
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
