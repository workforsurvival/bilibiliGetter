import time, requests, re, json, datetime
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from _init import funcInit
from _mHelper import mysql_helper

cInit = funcInit()
driver = cInit.set_driver()
# set region
file_name = "data"
# 1-417
inserted = 0


# https://www.bilibili.com/v/popular/rank/all
# ==> href="//www.bilibili.com/video/BV1wi4y1T7jZ"
# ==> title : //*[@id="viewbox_report"]/h1/span
# ==> creator : //*[@id="v_upinfo"]/div[1]/a
# ==> tmCount : //*[@id="bilibiliPlayer"]/div[1]/div[2]/div/div[1]/div[2]/span[2]
# ==> info : //*[@id="v_desc"]/div[2]
# ==> tags : //*[@id="v_tag"]/ul/li[1]/div/a/span
# ==> addCount : //*[@id="comment"]/div/div[1]/span[1]
# ==> comment : p==text
# ==> recommnet : span == text-con


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
        # links.append(link['href'])
        # cid = 'BV1vz4y1C7TS'
        url = "https://www.bilibili.com/video/" + cid
        ######################### timeout error
        driver.get(url)
        while driver.page_source == False:
            print("internet connection error, try again later 3 second..")
            time.sleep(3)
            driver.get(url)
        try:
            if bool("404 Not Found" in driver.page_source):
                # print("--404: "+ data['cid'])
                # imy.exec("delete from Product where cid=%s",(data['cid']))
                pass
            else:
                driver.execute_script("window.scrollTo(0,1080)")
                time.sleep(1)
                driver.execute_script("window.scrollTo(0,1080)")

                title = driver.find_element_by_xpath(
                    '//*[@id="viewbox_report"]/h1/span'
                ).text
                creator = driver.find_element_by_xpath(
                    '//*[@id="v_upinfo"]/div[2]/div[1]/a[1]'
                ).get_attribute("href")
                tmCount = driver.find_element_by_xpath(
                    '//*[@id="viewbox_report"]/div/span[2]'
                ).text
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
                _comments = driver.find_elements_by_class_name("text")
                for comment in _comments:
                    comments.append(comment.text)
                _recomments = driver.find_elements_by_class_name("text-con")
                for recommend in _recomments:
                    recomments.append(recommend.text)
                ###########################################################################################
                # page 1 to all
                ############################################################################################
                # Next 버튼 클릭
                # 새로운 페이지 있는지 판단
                # 새로운 페이지일시 다시 코멘츠를 짤라 넣기
                # totalPage = driver.find_elements_by_class_name("tcd-number")[-1].text
                # tPage = int(totalPage)
                print('🏌️‍♂️[%s] ⌸ %s ' % (cid,title))
                tPage = 1000
                if tPage > 0:
                    p = 1
                    while p < tPage:
                        try:
                            if bool("class=\"next\">下一页</a>" in driver.page_source):
                                nextPageBtn = driver.find_element_by_class_name("next")
                                nextPageBtn.click()
                                # nowPage = int(
                                #     driver.find_element_by_class_name("current").text
                                # )
                                # if bool(p + 1 == nowPage):
                                _comments = driver.find_elements_by_class_name("text")
                                for comment in _comments:
                                    comments.append(comment.text)
                                # time.sleep(0.3)
                                _recomments = driver.find_elements_by_class_name("text-con")
                                for recommend in _recomments:
                                    recomments.append(recommend.text)
                                print(str(p)+',',end='')
                                p = p + 1
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
                print("[" + str(i) + "] done: " + item["title"])
                fileName = cid + ".json"
                # json파일로 저장
                with open(fileName, "w") as json_file:
                    json.dump(item, json_file)
                    print("file copyed %s" % (cid))
                items.append(item)
                i = i + 1
        except OSError as err:
            print("OS error: {0}".format(err))
            pass

    # print("done : ["+str(page)+"]p - ["+str(inserted)+"] (inserted)")
except:
    # print("pass: page -- ["+str(page)+"] ")
    pass