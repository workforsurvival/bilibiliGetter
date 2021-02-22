import time,requests,re,json,math
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from _init import funcInit
from _mHelper import mysql_helper

cInit = funcInit()
driver = cInit.set_driver()
# set region
#1-417

######################################################################################################
## Translate
#cInit.initTrans(driver,'Product','_title')
cInit.initTrans(driver,'Product','_product_discription')
#cInit.initTrans(driver,'Actor','_name')
#cInit.initTrans(driver,'Genre','_name')
cInit.initTrans(driver,'Director','_name')
cInit.initTrans(driver,'Maker','_name')
cInit.initTrans(driver,'Label','_name')
cInit.initTrans(driver,'Series','_name')
######################################################################################################




