import re,json,os,glob,jieba
from _mHelper import mysql_helper

# dbSelect Data
imy = mysql_helper()
types = [1,2]
for type in types:
    recs = imy.getRecords(type)
    # dbCut Word and insert data
    for rec in recs:
        try:
            cuts = jieba.cut(rec['comment'],use_paddle=True)
            for cut in cuts:
                imy.insertR("insert into words set cid=%s,words=%s",(rec['cid'],cut))
                # print('cut')
            imy.updateR("update comments set type=3 where cid=%s",(rec['cid']))            
            print('rec done:[%s]'%rec)
        except OSError as err:
            print('--- err: %s' % err)
            pass
    print('type done:[%s]'%type)
    # if have word + 1 update
    # else insert data
    # insert into words set cid='BV1wi4y1T7jZ',words='sum';
    # update words set count=count+1 where cid='BV1wi4y1T7jZ';