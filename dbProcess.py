import re,json,os,glob
from _mHelper import mysql_helper

### 0. 사용되는 함수와 변수들
# video,manga,webtoon,picture,novel
folders = ['jdata']
for folder in folders:
    imy = mysql_helper()
    ### 1. 폴더밑에 파일을 읽는다.
    localRoot = '%s/%s/' % (os.getcwd(),folder)
    files = glob.glob("%s*.json" % localRoot)
    #files = sorted(files,key=lambda name: int(name[len(localRoot):-5]))
    files.sort(key=os.path.getctime)
    for file in files:
        with open(file,"r") as json_file:
            ### 2. 파일을 json으로 바꾼다
            try:
                json_data = json.load(json_file)
                cid=json_data['cid']
                title=json_data['title']
                creator=json_data['cid']
                tmCount=json_data['tmCount']
                info=json_data['cid']
                addCount=json_data['addCount']
                tags = json.dumps(json_data['tags'])

                queryString = "insert into contents set cid=%s,creator=%s,title=%s,tags=%s,info=%s,addCount=%s"
                tup = [cid,creator,title,tags,info,addCount]
                # 테이블에 id가 같은거 있는지 체크, 없을시 insert
                if imy.selectCount("contents",'cid',json_data['cid']) == 0:
                    imy.insertR(queryString,tup)
                    for comment in json_data['comments']:
                        tup=[cid,comment]
                        queryString = "insert into comments set cid=%s,comment=%s,type=1"
                        imy.insertR(queryString,tup)
                    for recomment in json_data['recomments']:
                        tup=[cid,recomment]
                        queryString = "insert into comments set cid=%s,comment=%s,type=2"
                        imy.insertR(queryString,tup)
                print("--done"+json_data['title'])
            except Exception as e:
                print(str(e))
        if os.path.exists(file):
            os.remove(file)
        print("--%s"%file)
            
