import time,requests,re,json
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from _init import funcInit
from _mHelper import mysql_helper

cInit = funcInit()
imy = mysql_helper()
driver = cInit.set_driver()
domain = 'https://nzhx.xyz'
t = 5
#1-200000
cid=4783
#cid=4502
while cid<300000:
    url = domain+"/index.php/vod/detail/id/"+str(cid)+".html"
    try:
        # 10초를 추가한 이유는 6초이내 이미지 로딩이 되지 않는다
        driver.set_page_load_timeout(t+10)
        driver.get(url)
    except:
        driver.execute_script("window.stop()")
    if driver.page_source:
        # BeautifulSoup으로 html형식을 쉽게 찾기 하기 위한 문구.
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # 콘텐츠에 포함된 비디오 링크 있을시 계속 없으면 패스
        #isTrueVideo = soup.find('div',{'class':'play-list'})
        isTrueVideo = driver.find_element_by_xpath('//*[@id="mp4play"]/div[2]/a[1]')
        if isTrueVideo:
            # url 
            url = isTrueVideo.get_attribute('href')
            # 태그는 h1밑의 a 태그들을 찾아본다.
            tags = driver.find_element_by_css_selector('#mainbody > div.container > div > div > div.player_title > div > a:nth-child(3)')
            if tags:
                tags = tags.text
            # 타이틀 ==> 중문 
            #default_title = soup.find('dt',{'class':'name'})
            default_title = driver.find_element_by_css_selector('#mainbody > div.container > div > div > div.player_title > h1')
            if default_title:
                default_title = default_title.text
            # 섬네일
            #thumbnail = soup.find('div',{'class':'ct-l'}).find('img')
            thumbnail = driver.find_element_by_xpath('//*[@id="main"]/div[1]/div/div[1]/img')
            if thumbnail:
                thumbnail = thumbnail.get_attribute('src')
            # HD인지 판단
            file_type = ''
            # file_type = soup.find('span',{'class':'bz'})
            # if file_type:
            #     file_type = file_type.text
            # 튜플로 묶어서 Contents에 삽입
            tup = (str(cid),default_title,thumbnail,file_type)
            # checkMainInsert은 지정필트에 값이 존재여부를 확인하고 입력함.==>중복데이타입력을 막음과 동시 에러가 나오지 않게 하기 위함.
            contents_id = imy.checkMainInsert('Contents','cid',cid,"insert into Contents set cid=%s,default_title=%s,thumbnail=%s,file_type=%s,description=''",tup)
            # Tags 메인 테이블 입력
            tags_id = imy.checkMainInsert('Tags','tagName',tags,"insert into Tags set tagName=%s,is_menu=1",(tags))
            # contents_tags FK테이블입력
            imy.checkFKInsert('contents_tags','contents_id',contents_id,'tags_id',tags_id,"insert into contents_tags set contents_id=%s,tags_id=%s",(contents_id,tags_id))
            # Contents와 Tags의 FK 테이블 입력
            
            # 이부분은 driver.get(url)시 시간이 30초 지남에도 페이지는 로딩되었는데 부분 js파일이 로딩되지 않아 페이지가 지연이 생긴다.
            # 해결 방법은 try except로 지정시간 6초지나서도 페이지 로딩이 되지 않으면 execute_script==>window.stop()로 강제로 브라우저 스톱시킨다.
            try:
                driver.set_page_load_timeout(t)
                driver.get(url)
            except:
                #print("load page too late. stopping get page actions..")
                driver.execute_script("window.stop()")
            # 가져온 텍스트중에 짜를 문자열을 포함하는지 판단.
            if bool('url":"http' in driver.page_source) and bool('.m3u8' in driver.page_source):
                # get_spec_str은 string에서 지정 문자열부터 지정문자열까지 끊어서 반환한다.
                resultText = cInit.get_spec_str(driver.page_source,'url":"http','.m3u8"').replace('\\','')
                # Links입력 후 contents_links에도 입력
                link='http'+resultText+'.m3u8'
                links_id = imy.checkMainInsert('Links','link',link,"insert into Links set link=%s",(link))
                imy.checkFKInsert('contents_links','contents_id',contents_id,'links_id',links_id,"insert into contents_links set contents_id=%s,links_id=%s",(contents_id,links_id))
        else:
            print("cid:" +str(cid)+" none video.")
    print("["+str(cid)+"]: "+default_title)
    cid=cid+1

