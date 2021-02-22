import time,requests,re,json
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from _init import funcInit
from _mHelper import mysql_helper

cInit = funcInit()
driver = cInit.set_driver()
# set region
regionTF = cInit.set_region(driver)
file_name = 'data'
#1-417
page=40
inserted=0

while page>0:
    tdatas = []
    url = 'https://www.dmm.co.jp/digital/videoa/-/list/=/sort=date/view=text/page='+str(page)+'/'
    try:
        driver.get(url)
        if regionTF==False:
            set_region(driver)
        while driver.page_source == False:
            print("internet connection error, try again later 3 second..")
            time.sleep(3)
            driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        links = []
        bo_tits = soup.find_all('p',{'class':'ttl'})
        for bo_tit in bo_tits:
            link = bo_tit.find('a')
            cid = re.findall(r'cid=\w{0,50}',link['href'])[0].replace("cid=","")
            links.append(cid)
            # links.append(link['href'])
    except:
        print("pass: page -- ["+str(page)+"] ")
        pass
    imy = mysql_helper()
    isI = 0
    for link in links:
        _cnt = imy.selectCount("Product","cid",link)
        if _cnt==0:
            isI = isI+1
            imy.insertR("insert into Product set cid=%s,c_date=now()",(link))
    page=page-1
    print("done: ["+str(page+1)+"] p - ("+str(isI)+") inserted")
    time.sleep(2)
