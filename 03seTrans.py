from bs4 import BeautifulSoup
import time,requests,re,json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from _init import funcInit
from _mHelper import mysql_helper

def initTrans(driver,transTable,transField):
    imy = mysql_helper()
    cInit = funcInit()
    ja_RealField = "ja"+transField
    ko_RealField = "ko"+transField
    cn_RealField = "cn"+transField
    en_RealField = "en"+transField
    datas = imy.getTrans(transTable,ko_RealField)
    for data in datas:
        try:
            ko = cInit.naverTrans(driver,"ja","ko",data[ja_RealField])
            # cn = cInit.baiduTrans(driver,"ja","cn",data[ja_RealField])
            en = cInit.googleTrans(driver,"ja","en",data[ja_RealField])

            imy.updateR("update "+transTable+" set "+ko_RealField+"=%s,"+en_RealField+"=%s where uid=%s",(ko,en,data['uid']))
            print("Done : "+transTable+"-"+ko)
        #except OSError as err:
        except:
            # print("OS error: {0}".format(err))
            print("Pass : "+transTable+"-"+data[ja_RealField])
            pass

cInit = funcInit()
driver = cInit.set_driver()

cInit.initTrans(driver,'Product','_title') 
cInit.initTrans(driver,'Product','_product_discription')
cInit.initTrans(driver,'Label','_name')
cInit.initTrans(driver,'Series','_name')