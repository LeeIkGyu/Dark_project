from ast import keyword
from bs4 import BeautifulSoup
from pymongo import MongoClient
import traceback
import requests
import re
import zlib
import threading
import dark_Crawler
import basics_category
from pytz import timezone
from datetime import datetime
import Snipping_Crawler
import basics_keyword


fmt = "%Y-%m-%d %H:%M:%S %Z%z"

ANY_URL_REGEX = "^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\W\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"

session = requests.session()
session.proxies = {'http': 'socks5h://localhost:9150',
                    'https': 'socks5h://localhost:9150'}

def info_return(htmlcode):
    title = 'None'
    lang = 'None'
    
    if htmlcode.find('title') is not None:
        title = htmlcode.find('title').get_text().encode('utf-8')
    elif htmlcode.find('TITLE') is not None:
        title = htmlcode.find('TILE').get_text().encode('utf-8')
        
    try:
        if htmlcode.find("html")["lang"]:
            lang = htmlcode.find("html")["lang"]
    except Exception as e:
        lang = 'en'
    
    return title, lang

def category_return(lang, text):
    category = ""
    
    if lang == 'en':
        category = basics_category.analysis(text).enC()
    elif lang == 'ko-KR':
        category = basics_category.analysis(text).koC()
    elif lang == 'ja':
        category = basics_category.analysis(text).jaC()
    elif lang == 'zh-CN':
        category = basics_category.analysis(text).chC()
    elif lang == 'ru':
        category = basics_category.analysis(text).ruC()
    else:
        category = basics_category.analysis(text).enC()
        
    return category

def analysis(url):
    status = 'None'
    server = 'None'
    title = 'None'.encode('utf-8')
    code = 'None'.encode('utf-8')
    category = ""
    lang = ""
    nowtime = datetime.now(timezone('Asia/Seoul')).strftime(fmt)[:19]
    
    try:
        res = session.get(url, timeout=10, headers={"Connection" : "close"})
        status = res.status_code
        requests_txt = res.text

        Soup = BeautifulSoup(requests_txt, "html.parser")

        title, lang = info_return(Soup)

        if Soup.find('html') is not None:
            code = str(Soup.find('html')).encode('utf-8')
        else:
            code = requests_txt.encode("utf-8")

        category = category_return(lang, title.decode('utf-8'))

        if category == "unknown":
            category = category_return(lang, requests_txt)
            if category == "unknown":
                category = "unknown"

        if 'server' in list(res.headers.keys()):
            server=res.headers['server']    
        elif 'Server' in list(res.headers.keys()):
            server=res.headers['Server']

        code=zlib.compress(code)
        url_box = []
        for a_tag in (Soup.find_all('a', href=True)):
            url_box.append(a_tag['href'])
        for form_tag in (Soup.find_all('form', action=True)):
            url_box.append(form_tag['action'])
        for iframe_tag in (Soup.find_all('iframe', src=True)):
            url_box.append(iframe_tag['src'])
        for img_tag in (Soup.find_all('img', src=True)):
            url_box.append(img_tag['src'])
        if(len(url_box)>=2):
            url_box=list(set(url_box))

        onion_box=[]

        for url_one in url_box:
            if re.findall(ANY_URL_REGEX, url_one)!=[]:
                if url_one.find('.onion')>=0:
                    onion_box.append(url_one)

        onion_box = list(set(onion_box))
        return category, url, nowtime, status, server, code, title, lang, onion_box

    except requests.exceptions.ConnectionError as e:
		# Sockect is max Error
        return 'unknown', url, nowtime,'unknown','unknown','unknown','unknown','unknown','unknown'

    except requests.exceptions.ReadTimeout as e:
		# Connect fail (time out)
        return 'unknown', url, nowtime,'unknown','unknown','unknown','unknown','unknown','unknown'
    
    except Exception as e:
        # Error
        return 'unknown', url, nowtime,'unknown','unknown','unknown','unknown','unknown','unknown'

def DBupload(url, engine, keyword, recursion_count):
    category, url, nowtime, status, server, code, title, lang, onion_box = analysis(url)

    if category == "unknown":
        category = keyword
    
    if status != 'unknown':
        if category != 'child porn':
            img = Snipping_Crawler.snap(url, category, keyword, nowtime)
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



def ResultToServer(onion_info, word):
    recursion_count=0
    for onion_url in onion_info.keys():
        onion_engine=onion_info[onion_url]
        DBupload(onion_url,onion_engine,word,recursion_count)

def en(key):
    for Word in key:
        for basics in basics_keyword.enC[Word]:
            search_class=dark_Crawler.basics_parser(basics,session)
            dicts={}
            ahmiavalue={'ahmia':search_class.ahmia()}
            torSearchvalue={'torSearch':search_class.tor()}
            dicts.update(dark_Crawler.Deduplication(torSearchvalue,ahmiavalue))
            ResultToServer(dicts, basics)

def ko(key):
    for Word in key:
        for basics in basics_keyword.koC[Word]:
            search_class=dark_Crawler.basics_parser(basics,session)
            dicts={}
            ahmiavalue={'ahmia':search_class.ahmia()}
            torSearchvalue={'torSearch':search_class.tor()}
            dicts.update(dark_Crawler.Deduplication(torSearchvalue,ahmiavalue))
            ResultToServer(dicts, basics)

def ja(key):
    for Word in key:
        for basics in basics_keyword.jaC[Word]:
            search_class=dark_Crawler.basics_parser(basics,session)
            dicts={}
            ahmiavalue={'ahmia':search_class.ahmia()}
            torSearchvalue={'torSearch':search_class.tor()}
            dicts.update(dark_Crawler.Deduplication(torSearchvalue,ahmiavalue))
            ResultToServer(dicts, basics)

def ch(key):
    for Word in key:
        for basics in basics_keyword.chC[Word]:
            search_class=dark_Crawler.basics_parser(basics,session)
            dicts={}
            ahmiavalue={'ahmia':search_class.ahmia()}
            torSearchvalue={'torSearch':search_class.tor()}
            dicts.update(dark_Crawler.Deduplication(torSearchvalue,ahmiavalue))
            ResultToServer(dicts, basics)

def ru(key):
    for Word in key:
        for basics in basics_keyword.ruC[Word]:
            search_class=dark_Crawler.basics_parser(basics,session)
            dicts={}
            ahmiavalue={'ahmia':search_class.ahmia()}
            torSearchvalue={'torSearch':search_class.tor()}
            dicts.update(dark_Crawler.Deduplication(torSearchvalue,ahmiavalue))
            ResultToServer(dicts, basics)

if __name__ == "__main__":
    print("[*] Start [*]")
    
    if __name__ == "__main__":
        print("[*] Start [*]")
    
    key = basics_keyword.key
    crawler_t1 = threading.Thread(target=en, args=(key,))
    crawler_t2 = threading.Thread(target=ko, args=(key,))
    crawler_t3 = threading.Thread(target=ja, args=(key,))
    crawler_t4 = threading.Thread(target=ch, args=(key,))
    crawler_t5 = threading.Thread(target=ru, args=(key,))

    crawler_t1.start()
    crawler_t2.start()
    crawler_t3.start()
    crawler_t4.start()
    crawler_t5.start()