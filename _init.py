import time,requests,re,json
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from _mHelper import mysql_helper

# ==========================================================================================================
# Func Area
# ==========================================================================================================
class funcInit:
    def set_driver(self):
        header = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }
        options = webdriver.ChromeOptions()
        #options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1200x600")
        options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        driver = webdriver.Chrome(ChromeDriverManager().install(),
                chrome_options=options,)
        driver.implicitly_wait(15)
        return driver
        
    def set_region(self,driver):
        print("try search region image button..")
        # if region is false, true 될때까지 계속 찾아보기
        driver.get('https://www.dmm.co.jp/')
        tcount = 0
        while driver.page_source == False:
            print("internet connection error, try again later 3 second..")
            time.sleep(3)
            driver.get(url)
        while bool(driver.find_elements_by_xpath("//*[@id=\"welcome\"]/div[2]/ul/li[2]/a/img"))==False:
            tcount=tcount+1
            if(tcount>5):
                print("try counter is over 5. break this while")
                return False
            print("try again 3 sec..")
            time.sleep(3)
            if bool(driver.find_elements_by_xpath("/html/body"))==True:
                time.sleep(3)
                driver.find_elements_by_xpath("/html/body")[0].click()
        python_button = driver.find_elements_by_xpath("//*[@id=\"welcome\"]/div[2]/ul/li[2]/a/img")[0]
        python_button.click()
        print("init program ok . start data getting.")
        return True

    def click_button(self,driver,xpath):
        if driver.find_elements_by_xpath(xpath):
            python_button = driver.find_elements_by_xpath(xpath)[0]
            time.sleep(1)
            python_button.click()
        return driver

    def get_spec_str(self,s_string,start,end):
        if bool(start in s_string) and bool(end in s_string):
            regex = re.compile(start+"(.*?)"+end)
            str_list = regex.findall(s_string)
            if len(str_list)>0:
                return str_list[0]
        return ""

    def get_content_video(self,cid):
        header = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }
        url = "https://www.dmm.co.jp/service/digitalapi/-/html5_player/=/cid="+cid+"/mtype=AhRVShI_/service=digital/floor=videoa/mode=/"
        #url = "https://www.dmm.co.jp/digital/videoa/-/detail/=/cid="+cid+"/?i3_ref=list&i3_ord=61"
        str_source = requests.get(url,headers=header,timeout=10).text
        # soup = BeautifulSoup(str_source, 'html.parser')
        # src":"\\/\\/cc3001.dmm.co.jp\\/litevideo\\/freepv\\/m\\/mir\\/mird00141\\/mird00141_dmb_w.mp4","title":
        return self.get_spec_str(str_source,"src\":\"","\",\"")
        #regex = re.compile("src\":\"(.*?)\",\"")
        #src_list = regex.findall(str_source)
        #if len(src_list)>0:
            #return "https:"+src_list[0]
        #return ""

    def put_array(self,arr_string):
        arrs = []
        for arr in arr_string:
            _id = self.get_spec_str(arr['href'],"id=","/")
            if _id:
                arr = {
                    "id":_id,
                    "name":arr.text,
                }
                arrs.append(arr)
        return arrs

    def naverTrans(self,driver,sk,tk,st):
        url = "https://papago.naver.com/?sk="+sk+"&tk="+tk+"&hn=0&st="+st
        driver.set_page_load_timeout(10)
        driver.get(url)
        while driver.page_source == False:
            print("internet connection error, try again later 3 second..")
            time.sleep(3)
            driver.get(url)
        result = driver.find_element_by_css_selector("div#txtTarget")
        count=0
        while bool(result.text) == False:
            time.sleep(1)
            result = driver.find_element_by_css_selector("div#txtTarget")
            count=count+1
            if count == 5:
                break
        if bool(result):
            return result.text
        else:
            return ""

    def googleTrans(self,driver,sk,tk,st):
        url = "https://translate.google.co.kr/?hl=ko#view=home&op=translate&sl="+sk+"&tl="+tk+"&text="+st
        driver.get(url)
        while driver.page_source == False:
            print("internet connection error, try again later 3 second..")
            time.sleep(3)
            driver.get(url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        result = soup.find('span',{'class':'tlid-translation translation'})
        count=0
        while bool(result.text) == False:
            time.sleep(1)
            result = soup.find('span',{'class':'tlid-translation translation'})
            count=count+1
            if count == 5:
                break
        if bool(result):
            return result.text
        else:
            return ""

    def baiduTrans(self,sk,tk,st):
        if sk=="ja":
            sk="jp"
        if tk=="cn":
            tk="zh"
        url="https://fanyi.baidu.com/#"+sk+"/"+tk+"/"+st
        driver.set_page_load_timeout(10)    
        driver.get(url)
        while driver.page_source == False:
            print("internet connection error, try again later 3 second..")
            time.sleep(3)
            driver.get(url)
        time.sleep(1)
        if bool(driver.find_elements_by_xpath("//*[@id=\"translate-button\"]")):
            btnOK = driver.find_elements_by_xpath("//*[@id=\"translate-button\"]")[0]
            btnOK.click()
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            result = soup.find('p',{'class':'ordinary-output target-output clearfix'})
            if bool(result):
                return result.text
            else:
                return ""

    def initTrans(self,driver,transTable,transField):
        imy = mysql_helper()
        ja_RealField = "ja"+transField
        ko_RealField = "ko"+transField
        cn_RealField = "cn"+transField
        en_RealField = "en"+transField
        datas = imy.getTrans(transTable,ko_RealField,ja_RealField)
        for data in datas:
            try:
                ko = self.naverTrans(driver,"ja","ko",data[ja_RealField])
                # cn = self.baiduTrans(driver,"ja","cn",data[ja_RealField])
                en = self.googleTrans(driver,"ja","en",data[ja_RealField])

                imy.updateR("update "+transTable+" set "+ko_RealField+"=%s,"+en_RealField+"=%s where uid=%s",(ko,en,data['uid']))
                print("Done : "+transTable+"-"+ko)
            #except OSError as err:
            except:
                # print("OS error: {0}".format(err))
                print("Pass : "+transTable+"-"+data[ja_RealField])
                pass


# ==========================================================================================================
# End -- Func Area
# ==========================================================================================================