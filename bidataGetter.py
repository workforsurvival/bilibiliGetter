import time, requests, re, json, datetime,sys
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from _init import funcInit
from _mHelper import mysql_helper

cInit = funcInit()
driver = cInit.set_driver()
# set region
# 1-417

limitPageNum = 10

if limitPageNum <= 0:
    print('argv value is false.')
    exit()


tdatas = []
url = "https://www.bilibili.com/v/popular/rank/all"
try:
    driver.get(url)
    while driver.page_source == False:
        print("internet connection error, try again later 3 second..")
        time.sleep(3)
        driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    links = []
    items = []
    bo_tits = soup.find_all("a", {"class": "title"})
    i = 0
    for bo_tit in bo_tits:
        cid = re.findall(r"video/\w{0,50}", bo_tit["href"])[0].replace("video/", "")
        links.append(cid)
        i=i+1
    # cids.json으로 링크만 저장한다.
    with open('cids.txt', "w") as cidsFile:
        for item in links:
            cidsFile.write("%s\n" % item)
        print("file copyed %s" % (str(i)))
    cids = []
    with open('cids.txt','r') as f:
        cids = f.readlines()
    for cid in cids:
        cid = cid.replace('\n','')
        url = "https://www.bilibili.com/video/" + cid
        ######################### timeout error
        driver.get(url)
        while driver.page_source == False:
            print("internet connection error, try again later 3 second..")
            time.sleep(3)
            driver.get(url)
        try:
            time.sleep(7)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(7)
            if bool("class=\"next\">下一页</a>" in driver.page_source):
                title = driver.find_element_by_xpath('//*[@id="viewbox_report"]/h1/span').text
                # creator = driver.find_element_by_xpath('//*[@id="v_upinfo"]/div[2]/div[1]/a[1]').get_attribute("href")
                # tmCount = driver.find_element_by_xpath('//*[@id="viewbox_report"]/div/span[2]').text
                creator = ""
                tmCount = driver.find_element_by_xpath('//*[@id="viewbox_report"]/div/span[2]').text
                info = driver.find_element_by_xpath('//*[@id="v_desc"]/div[2]').text
                addCount = driver.find_element_by_xpath(
                    '//*[@id="comment"]/div/div[1]/span[1]'
                ).text

                tags = []
                _tags = driver.find_elements_by_class_name("tag")
                for tag in _tags:
                    tags.append(tag.text)
                comments = []
                recomments = []
                # _comments = driver.find_elements_by_class_name("text")
                # for comment in _comments:
                #     comments.append(comment.text)
                # _recomments = driver.find_elements_by_class_name("text-con")
                # for recommend in _recomments:
                #     recomments.append(recommend.text)
                ###########################################################################################
                # page 1 to all
                ############################################################################################
                # Next 버튼 클릭
                # 새로운 페이지 있는지 판단
                # 새로운 페이지일시 다시 코멘츠를 짤라 넣기
                # totalPage = driver.find_elements_by_class_name("tcd-number")[-1].text
                # tPage = int(totalPage)
                print('🏌️‍♂️[%s] ⌸ %s ' % (cid,title))
                tPage = limitPageNum
                if tPage > 0:
                    p = 1
                    while p < tPage:
                        try:
                            if bool("class=\"next\">下一页</a>" in driver.page_source and i!=1):
                                driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                                time.sleep(0.1)
                                for comment in driver.find_elements_by_class_name("text"):
                                    comments.append(comment.text)
                                time.sleep(0.1)
                                for recommend in driver.find_elements_by_class_name("text-con"):
                                    recomments.append(recommend.text)
                                # print(str(p)+',',end='')
                                print(str(p))
                                p = p + 1
                                driver.find_element_by_class_name("next").click()
                                time.sleep(0.2)
                            else:
                                break
                        except Exception as err:
                            print("OS error: {0}".format(err))
                            p = p + 1
                            pass
                item = {
                    "cid": cid,
                    "title": title,
                    "creator": creator,
                    "tmCount": tmCount,
                    "info": info,
                    "addCount": addCount,
                    "tags": tags,
                    "comments": comments,
                    "recomments": recomments,
                }
                print(" done: " + item["title"])
                fileName = "./jdata/%s.json" % cid
                # json파일로 저장
                if(len(comments)>20):
                    with open(fileName, "w") as json_file:
                        json.dump(item, json_file)
                        print("file copyed %s" % (cid))
                    items.append(item)
        except OSError as err:
            print("OS error: {0}".format(err))
            pass

    # print("done : ["+str(page)+"]p - ["+str(inserted)+"] (inserted)")
except OSError as err:
    # print("pass: page -- ["+str(page)+"] ")
    print("OS error: {0}".format(err))
    pass