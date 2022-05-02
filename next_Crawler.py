from ast import keyword
from bs4 import BeautifulSoup
import requests
import re
import dark_Crawler
import basics_category
from pytz import timezone
from datetime import datetime
import Snipping_Crawler
from pymongo import mongo_client
import traceback
import keyword

fmt = "%Y-%m-%d %H:%M:%S %Z%z"

ANY_URL_REGEX = "^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\W\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"

session = requests.session()
session.proxies = {'http':  'socks5h://localhost:9050',
            'https': 'socks5h://localhost:9050'}

def info_return(htmlcode):
    title = ""
    lang = ""
    
    if htmlcode.find('title')>=0:
        title = htmlcode.find('title').get_text()
    elif htmlcode.find('TITLE')>=0:
        title = htmlcode.find('TILE').get_text()
        
    if htmlcode.find('html', lang = True)>=0:
        lang = htmlcode.find('html', lang = True).get_text()
    else:
        lang = 'en'
    
    return title, lang

def category_return(lang, text):
    category = ""
    
    if lang == 'en':
        category = basics_category.analysis(text).enC
    elif lang == 'ko-KR':
        category = basics_category.analysis(text).koC
    elif lang == 'ja':
        category = basics_category.analysis(text).jaC
    elif lang == 'zh-CN':
        category = basics_category.analysis(text).chC
    elif lang == 'ru':
        category = basics_category.analysis(text).ruC
    else:
        category = basics_category.analysis(text).enC
        
    return category

def analysis(url):
    status = ""
    server = ""
    title = ""
    code = "".encode('utf-8')
    category = ""
    lang = ""
    nowtime = datetime.now(timezone('Asia/Seoul')).srtftime(fmt)[:9]
    
    try:
        res = session.get(url, timeout=10, headers={"Connection" : "close"})
        status = res.status_code
        requests_txt = res.text
        
        Soup = BeautifulSoup(requests_txt, "html.parser")
        
        title, lang = info_return(Soup)
        
        if Soup.find('html')>=0:
            code = str(Soup.find('html')).encode('utf-8')
        else:
            code = requests_txt.encode("utf-8")
        
        category = category_return(lang, title)
        
        if category == "unknown":
            category = category_return(lang, requests_txt)
        
        if 'server' in list(res.headers.keys()):
            server=res.headers['server']    
        elif 'Server' in list(res.headers.keys()):
            server=res.headers['Server']
        
        url_box = []
        for a_tag in (Soup.fina_all('a', href=True)):
            url_box.append(a_tag['href'])
        for form_tag in (Soup.fina_all('form', action=True)):
            url_box.append(form_tag['action'])
        for iframe_tag in (Soup.fina_all('iframe', src=True)):
            url_box.append(iframe_tag['src'])
        for img_tag in (Soup.fina_all('img', src=True)):
            url_box.append(img_tag['src'])
            
        onion_box=[]
        
        for url_one in url_box:
            if re.findall(ANY_URL_REGEX, url_one)!=[]:
                if url_one.find('.onion')>=0:
                    onion_box.append(url_one)
        
        oinon_box = list(set(onion_box))
        return category, url, nowtime, status, server, code, title, lang, onion_box
    
    except requests.exceptions.ConnectionError as e:
		# Sockect is max Error
        return 'unknown', url, nowtime,'unknown','unknown','unknown','unknown','unknown','unknown','unknown'

    except requests.exceptions.ReadTimeout as e:
		# Connect fail (time out)
        return 'unknown', url, nowtime,'unknown','unknown','unknown','unknown','unknown','unknown','unknown'
    
    except Exception as e:
        # Error
        return 'unknown', url, nowtime,'unknown','unknown','unknown','unknown','unknown','unknown','unknown'
    
def DBupload(url, engine, keyword, recursion_count):
    category, url, nowtime, status, server, code, title, lang, onion_box = analysis(url)
    
    if status != 'unknown':
        if category != 'child porn':
            # img = Snipping_Crawler
            data = {'category':category,'keyword':keyword,'engine':engine,'url':url,'time':nowtime,'state':status,'server':server,'code':str(code),'img':img,'title':title,'language':lang}
        else:
            data = {'category':category,'keyword':keyword,'engine':engine,'url':url,'time':nowtime,'state':status,'server':server,'code':str(code),'title':title,'language':lang}
        
        DB_insert(data)
        
        if(recursion_count<=2 and type(onion_box)==list):
            if(url in onion_box):
                onion_box.remove(url)

			#recursion_start
            for urls in onion_box:
                DBupload(urls, engine, keyword, recursion_count+1)

def DB_insert(data): ## 데이터 추가, 삭제 및 변경 동작
        try:     
            client = MongoClient(host = 'localhost', port = 27017) 
            DWdb = client['DWMongodb'] ## db name     
            print('MongoDB - DWMongodb Connected Success') # 클라이언트(데베) 연결 성공 

            #데이터 입 력
            if len(data.keys()) == 11: # 포르노가 아닐 경우 
                CrawlingData= {
                    'Category' : data.get('category'),
                    'Keyword' : data.get('keyword'),
                    'Engine' : data.get('engine'),
                    'URL' : data.get('url'),
                    'Time' : data.get('time'),
                    'State' : data.get('state'),
                    'Server' : data.get('server'),
                    'Code' : data.get('code'),
                    'Title' : data.get('title'),
                    'Language' : data.get('language')
                }
            else: # 아동 포르노일 경우 
                CrawlingData = {
                    'Category' : data.get('category'),
                    'Keyword' : data.get('keyword'),
                    'Engine' : data.get('engine'),
                    'URL' : data.get('url'),
                    'Time' : data.get('time'),
                    'State' : data.get('state'),
                    'Server' : data.get('server'),
                    'Code' : data.get('code'),
                    'Img' : data.get('img'),
                    'Title' : data.get('title'),
                    'Language' : data.get('language')
                }
            
            CrawlingInfo_live = DWdb["CrawlingInfo_live"] # 실시간 데이터 들어갈 곳
            CrawlingInfo_add = DWdb["CrawlingInfo_add"] #  초기에 정한 카테고리 이외의 데이터 

            DWdb_Data = DWdb.CrawlingInfo_live.insert_one(CrawlingData) #데이터 삽입 
            print('Data Insert Success')           

        except:
            print('Error')
            print(traceback.format_exc())
            

def ResultToServer(onion_info, word):
    recursion_count=0
    for onion_url in onion_info.keys():
        onion_engine=onion_info[onion_url]
        DBupload(onion_url,onion_engine,word,recursion_count)

def main():
    print("[*] Start [*]")
    
    for Word in keyword.key:
        # en
        search_class=dark_Crawler.basics_parser(keyword.enC[Word],session)
        dicts={}
        ahmiavalue={'ahmia':search_class.ahmia()}
        torSearchvalue={'torSearch':search_class.tor()}
        dicts.update(dark_Crawler.Deduplication(torSearchvalue,ahmiavalue))
        ResultToServer(dicts, keyword.enC[Word])
    
    for Word in keyword.key:
        # ko
        search_class=dark_Crawler.basics_parser(keyword.koC[Word],session)
        dicts={}
        ahmiavalue={'ahmia':search_class.ahmia()}
        torSearchvalue={'torSearch':search_class.tor()}
        dicts.update(dark_Crawler.Deduplication(torSearchvalue,ahmiavalue))
        ResultToServer(dicts, keyword.koC[Word])
    
    for Word in keyword.key:
        # ja
        search_class=dark_Crawler.basics_parser(keyword.jaC[Word],session)
        dicts={}
        ahmiavalue={'ahmia':search_class.ahmia()}
        torSearchvalue={'torSearch':search_class.tor()}
        dicts.update(dark_Crawler.Deduplication(torSearchvalue,ahmiavalue))
        ResultToServer(dicts, keyword.jaC[Word])
    
    for Word in keyword.key:
        # ch
        search_class=dark_Crawler.basics_parser(keyword.chC[Word],session)
        dicts={}
        ahmiavalue={'ahmia':search_class.ahmia()}
        torSearchvalue={'torSearch':search_class.tor()}
        dicts.update(dark_Crawler.Deduplication(torSearchvalue,ahmiavalue))
        ResultToServer(dicts, keyword.chC[Word])
    
    for Word in keyword.key:
        # ru
        search_class=dark_Crawler.basics_parser(keyword.ruC[Word],session)
        dicts={}
        ahmiavalue={'ahmia':search_class.ahmia()}
        torSearchvalue={'torSearch':search_class.tor()}
        dicts.update(dark_Crawler.Deduplication(torSearchvalue,ahmiavalue))
        ResultToServer(dicts, keyword.ruC[Word])

if __name__ == "__main__":
    main()