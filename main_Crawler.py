from bs4 import BeautifulSoup
import requests
import zlib
from Dark_project import dark_Crawler
from Dark_project import basics_category
from Dark_project import darK_log
from Dark_project import mongodb
from Dark_project import basics_keyword
from pytz import timezone
from datetime import datetime
import time
import threading
from multiprocessing import Process
import chardet

fmt = "%Y-%m-%d %H:%M:%S %Z%z"

ANY_URL_REGEX = "^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\W\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"

session = requests.session()
session.proxies = {'http': 'socks5h://localhost:9150',
                    'https': 'socks5h://localhost:9150'}

def info_return(htmlcode):
    title = 'None'
    lang = 'None'
    
    if htmlcode.find('title') is not None:
        title = htmlcode.find('title').get_text()
    elif htmlcode.find('TITLE') is not None:
        title = htmlcode.find('TILE').get_text()
        
    try:
        if htmlcode.find("html")["lang"]:
            lang = htmlcode.find("html")["lang"]
    except Exception as e:
        lang = 'en'
    
    return title, lang

def category_return(lang, text, url):
    
    if lang == 'en':
        basics_category.analysis(text, url).enC()
    elif lang == 'ko-KR':
        basics_category.analysis(text, url).koC()
    elif lang == 'ja':
        basics_category.analysis(text, url).jaC()
    elif lang == 'zh-CN':
        basics_category.analysis(text, url).chC()
    elif lang == 'ru':
        basics_category.analysis(text, url).ruC()
    else:
        basics_category.analysis(text, url).enC()

def analysis(url):
    status = 'None'
    server = 'None'
    textcode = ""
    title = 'None'
    code = 'None'.encode('utf-8')
    lang = ""
    nowtime = datetime.now(timezone('Asia/Seoul')).strftime(fmt)[:19]
    
    try:
        res = session.get(url, headers={"Connection" : "close"})
        status = res.status_code
        requests_txt = res.text

        Soup = BeautifulSoup(requests_txt, "html.parser")

        title, lang = info_return(Soup)

        title_enco = chardet.detect(title.encode())
        title.encode(title_enco.get('encoding'))

        if Soup.find('html') is not None:
            code = str(Soup.find('html')).encode('utf-8')
            textcode = Soup.find('html').get_text()
        else:
            code = requests_txt.encode("utf-8")
            textcode = Soup.get_text()

        category_return(lang, requests_txt, url)

        if 'server' in list(res.headers.keys()):
            server=res.headers['server']    
        elif 'Server' in list(res.headers.keys()):
            server=res.headers['Server']
        
        logging = "[URL : {0}] [Time : {1}] [Status : {2}] [Server : {3}] [Title : {4}] [Lang : {5}]".format(url, nowtime, status, server, title, lang)
        code=zlib.compress(code)
        darK_log.log_info(logging)
        return url, nowtime, status, server, code, title, lang, textcode

    except requests.exceptions.ConnectionError as e:
		# Sockect is max Error
        darK_log.log_error(e)
        return url, nowtime,'unknown','unknown','unknown','unknown','unknown','unknown'

    except requests.exceptions.ReadTimeout as e:
		# Connect fail (time out)
        darK_log.log_error(e)
        return url, nowtime,'unknown','unknown','unknown','unknown','unknown','unknown'
    
    except Exception as e:
        # Error
        darK_log.log_error(e)
        return url, nowtime,'unknown','unknown','unknown','unknown','unknown','unknown'

def DBupload(url, engine, keyword):
    url, nowtime, status, server, code, title, lang, textcode = analysis(url)
    
    if status != 'unknown':
        data = {'url':url,'engine':engine,'state':status,'server':server,'keyword':keyword,'title':title,'language':lang,'code':code,'textcode':textcode,'time':nowtime}
        
        mongodb.DB_insert(data)
        
def ResultToServer(onion_info, word):
    thlist = []
    for onion_url in onion_info.keys():
        onion_engine=onion_info[onion_url]
        th = threading.Thread(target = DBupload, args = (onion_url,onion_engine,word))
        th.start()
        thlist.append(th)

    for thread in thlist:
                thread.join()

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
    start = time.perf_counter()

    key = basics_keyword.key
    crawler_t1 = Process(target=en, args=(key,))
    crawler_t2 = Process(target=ko, args=(key,))
    crawler_t3 = Process(target=ja, args=(key,))
    crawler_t4 = Process(target=ch, args=(key,))
    crawler_t5 = Process(target=ru, args=(key,))
    crawler_t1.start()
    crawler_t2.start()
    crawler_t3.start()
    crawler_t4.start()
    crawler_t5.start()
    
    crawler_t1.join()
    crawler_t2.join()
    crawler_t3.join()
    crawler_t4.join()
    crawler_t5.join()
    
    finish = time.perf_counter()
    
    print(f'Finished in {round(finish-start, 2)} second(s)')