import time,requests,re,json,math
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from _init import funcInit
from _mHelper import mysql_helper
########################################################################################################################################################
## 1. dmm ==> json
########################################################################################################################################################

cInit = funcInit()
driver = cInit.set_driver()
# set region
regionTF = cInit.set_region(driver)
 
# get ja_title is null
imy = mysql_helper()
limit = 20
total_count = imy.initCidCount()
total_pages = math.ceil(total_count/limit)
for page in range(1,total_pages):
    startLimit = (page-1)*limit
    datas = imy.initCids(startLimit,limit)
    #print("loading data: ["+str(page)+"]p - ["+str(len(datas))+"]")
    Items=[]
    ii=0
    for data in datas:
        ii=ii+1
        url = "https://www.dmm.co.jp/digital/videoa/-/detail/=/cid="+data['cid']+"/?i3_ref=list&i3_ord=49"
        ######################### timeout error
        driver.get(url)
        while driver.page_source == False:
            print("internet connection error, try again later 3 second..")
            time.sleep(3)
            driver.get(url)
        try:
            if bool("404 Not Found" in driver.page_source):
                print("--404: "+ data['cid'])
                imy.exec("delete from Product where cid=%s",(data['cid']))
                pass
            else:
                # show all actors
                if bool("a_performer" in driver.page_source):
                    cInit.click_button(driver,"//*[@id=\"a_performer\"]")
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                table = soup.find('table',{'class':'mg-b20'})

                title = soup.find('h1',{'id':'title'}).text
                distribution_date = table.find_all('tr')[2].select('td')[1].text.strip()
                product_date = table.find_all('tr')[3].select('td')[1].text.strip()
                recording_time = table.find_all('tr')[4].select('td')[1].text.strip()
                cid = data['cid']
                if bool(soup.find('span',{'class':'tx-count'}).find('span')):
                    ctr = soup.find('span',{'class':'tx-count'}).find('span').text.strip()
                else:
                    ctr = "0"
                star = table.find('img',{'class':'mg-r6 middle'})['src'].replace('https://p.dmm.co.jp/p/ms/review/','').replace('.gif','')
                post_image = soup.find('img',{'id':'package-src-'+cid})['src']
                if bool(soup.find('a',{'name':'package-image'})):
                    content_image = soup.find('a',{'name':'package-image'})['href']
                else:
                    content_image = ""
                content_video = cInit.get_content_video(cid)
                product_discription = soup.find('div',{'class':'mg-b20 lh4'}).text.strip()
                directors = cInit.put_array(table.find_all('tr')[6].select('td')[1].find_all('a'))
                series = cInit.put_array(table.find_all('tr')[7].select('td')[1].find_all('a'))
                maker = cInit.put_array(table.find_all('tr')[8].select('td')[1].find_all('a'))
                label = cInit.put_array(table.find_all('tr')[9].select('td')[1].find_all('a'))
                actors = cInit.put_array(table.find_all('tr')[5].select('td')[1].find_all('a'))
                genres = cInit.put_array(table.find_all('tr')[10].select('td')[1].find_all('a'))
                if bool(genres)==False:
                    genres = cInit.put_array(table.find_all('tr')[11].select('td')[1].find_all('a'))
                sample_images = []
                _sample_images = soup.find('div',{'id':'sample-image-block'})
                if(_sample_images):
                    _sample_images = _sample_images.find_all('img',{'class':'mg-b6'})
                    for _sample_image in _sample_images:
                        sample_images.append(_sample_image['src'])

                item = {
                    "title":title,
                    "distribution_date":distribution_date,
                    "product_date":product_date,
                    "recording_time":recording_time,
                    "actors":actors,
                    "directors":directors,
                    "series":series,
                    "maker":maker,
                    "label":label,
                    "genres":genres,
                    "cid":cid,
                    "tx_count":ctr,
                    "ctr":ctr,
                    "star":star,
                    "post_image":post_image,
                    "product_discription":product_discription,
                    "content_image":content_image,
                    "content_video":content_video,
                    "sample_images" : sample_images,
                }
                print('['+str(page)+' - '+str(ii)+']''done: '+data['cid'])
                Items.append(item)
        except:
            print('-- pass: '+data['cid'])
            pass


    for item in Items:
        inserted = 0
        try:
            if bool(item.get('title')):
                # Product Insert
                tup = (item['title'],item['distribution_date'],item['product_date'],item['recording_time'],item['star'],item['post_image'],item['content_image'],item['content_video'],item['product_discription'],item['ctr'],item['tx_count'],item['cid'])
                query = "update Product set ja_title=%s,distribution_date=%s,product_date=%s,recording_time=%s,star=%s,post_image=%s,content_image=%s,content_video=%s,ja_product_discription=%s,ctr=%s,tx_count=%s,is_inserted=1 where cid=%s"
                product_id = imy.ProductCheckUpdate(query,tup,item['cid'])

                def mtomDataSet(dicts,table_name,conn_table_name,product_id,conn_id_name):
                    imy = mysql_helper()
                    for _itm in dicts:
                        _id = imy.mm_check_insert(table_name,_itm['id'],_itm['name'])
                        if imy.checkMtoM(conn_table_name,product_id,conn_id_name,_id)==0:
                            imy.insertR("insert into "+conn_table_name+" set product_id=%s,"+conn_id_name+"=%s",(product_id,_id))

                def simgDataSet(dicts,product_id,cid):
                    imy = mysql_helper()
                    for _itm in dicts:
                        _id = imy.simg_check_insert(cid,_itm)
                        if imy.checkMtoM("Product_simgs",product_id,"simg_id",_id)==0:
                            imy.insertR("insert into Product_simgs set product_id=%s,simg_id=%s",(product_id,_id))
                mtomDataSet(item['actors'],"Actor","Product_actors",product_id,"actor_id")
                mtomDataSet(item['genres'],"Genre","Product_genres",product_id,"genre_id")
                mtomDataSet(item['directors'],"Director","Product_director",product_id,"director_id")
                mtomDataSet(item['maker'],"Maker","Product_maker",product_id,"maker_id")
                mtomDataSet(item['series'],"Series","Product_series",product_id,"series_id")
                mtomDataSet(item['label'],"Label","Product_label",product_id,"label_id")
                simgDataSet(item['sample_images'],product_id,item['cid'],)

                #imy.updateR("update Item set is_inserted=1 where id=%s",(item['id']))
                #print("Item Insert ok. cid :["+item['cid']+"]")
                inserted=inserted+1

        except:
            print("OS error: {0}".format(err))
            print("pass to  id:" + str(item['id']))
            pass
    print("done : ["+str(page)+"]p - ["+str(inserted)+"] (inserted)")