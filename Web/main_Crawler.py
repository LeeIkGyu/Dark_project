"""dark_Crawler에서 파싱한 URL들의 데이터를 파싱하는 모듈"""
from bs4 import BeautifulSoup
import requests
import zlib
import dark_Crawler
import basics_category
import darK_log
import mongodb
import basics_keyword
from pytz import timezone
from datetime import datetime
import time
import threading
from multiprocessing import Process
import chardet
import re
import warnings

"""
bs4에서 나오는 warning을 해결하기 위해 사용,
해당 warning은 제작 당시 발견된지 일주일 밖에 되지 않았기 때문에 제대로된 해결방안이 없었음
"""
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

fmt = "%Y-%m-%d %H:%M:%S %Z%z"

"""URL에서 .onion 이라는 문자만 추출하기 위해 정규식에서 사용하는 문자열"""
ANY_URL_REGEX = "^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\W\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"

"""Tor 사이트를 파싱하기 위해서는 Tor에서 사용하는 Proxy를 사용해야함"""
session = requests.session()
session.proxies = {'http': 'socks5h://localhost:9150',
                    'https': 'socks5h://localhost:9150'}

"""파싱한 html 데이터에서 title과 언어를 반환하는 함수"""
def info_return(htmlcode):
    title = 'None'
    lang = 'None'
    
    """html 데이터에서 title tag를 찾아서 title만 가져옴"""
    if htmlcode.find('title') is not None:
        title = htmlcode.find('title').get_text()
    elif htmlcode.find('TITLE') is not None:
        title = htmlcode.find('TILE').get_text()
    
    """
    html 데이터에서 html 태그를 찾아 태그 안에 lang 속성이 있는지 확인하고 있으면 언어를 추출하고 없으면 기본 언어를 en로 설정함
    기본 언어를 en으로 하는 이유는 다른 나라 언어가 아닌 영어로 작성된 사이트 들은 lang 속성을 잘 추가 하지 않기 때문
    """
    try:
        if htmlcode.find("html")["lang"]:
            lang = htmlcode.find("html")["lang"]
    except Exception as e:
        lang = 'en'
    
    return title, lang

"""
언어를 확인하고 basics_category 모듈의 analysis 함수의 인자값으로
html 데이터와 URL을 넘겨줌 analysis 함수에서는 카테고리를 지정하여 MongoDB에 URL과 함께 저장
"""
def category_return(lang, text, url):
    """ISO 639-1 표준의 국가별 언어 코드를 참고하여 해당 국가별 언어 코드인지 정규식으로 확인"""
    
    #영어
    if re.compile(lang, re.I).findall("en en-au en-bz en-ca en-ie en-jm en-nz en-za en-tt en-gb en-us"):
        basics_category.analysis(text, url).enC()
    #한국어
    elif re.compile(lang, re.I).findall("ko ko-kr"):
        basics_category.analysis(text, url).koC()
    #일본어
    elif re.compile(lang, re.I).findall("ja"):
        basics_category.analysis(text, url).jaC()
    #중국어
    elif re.compile(lang, re.I).findall("zh-hk zh-cn zh-sg zh-tw"):
        basics_category.analysis(text, url).chC()
    #러시아어
    elif re.compile(lang, re.I).findall("ru ru-md"):
        basics_category.analysis(text, url).ruC()
    #영어
    else:
        basics_category.analysis(text, url).enC()

"""
URL에서 데이터를 파싱하는 함수
파싱할 데이터는 URL, 파싱한 시간, status, server, html, 제목, 언어, 페이지의 문자열을 파싱하여 return
"""
def analysis(url):
    status = 'None'
    server = 'None'
    textcode = ""
    title = 'None'
    code = 'None'.encode('utf-8')
    lang = ""
    nowtime = datetime.now(timezone('Asia/Seoul')).strftime(fmt)[:19]
    
    """
    try로 먼저 URL로 접속이 가능한지 확인하고 접속이 불가능하거나 파싱 도중 except가 일어나면 
    dark_log의 log_error 함수로 except를 기록
    """
    try:
        res = session.get(url,timeout=10,headers={"Connection" : "close"})
        """
        status = status 정보
        requests_txt = 소스코드
        """
        status = res.status_code
        requests_txt = res.text

        """소스코드에서 html의 코드만 파싱"""
        Soup = BeautifulSoup(requests_txt, "html.parser")

        """title과 언어 정보를 html 코드에서 추출"""
        title, lang = info_return(Soup)

        """title이 러시아어로 되어 있으면 저장할 때 인코딩 오류를 일으키기 때문에 인코딩을 설정"""
        title_enco = chardet.detect(title.encode())
        title.encode(title_enco.get('encoding'))

        if Soup.find('html') is not None:
            code = str(Soup.find('html')).encode('utf-8')
            textcode = Soup.find('html').get_text()
        else:
            code = requests_txt.encode("utf-8")
            textcode = Soup.get_text()

        """URL의 카테고리를 지정"""
        category_return(lang, requests_txt, url)

        """헤더에서 서버 정보를 추출"""
        if 'server' in list(res.headers.keys()):
            server=res.headers['server']    
        elif 'Server' in list(res.headers.keys()):
            server=res.headers['Server']
        
        """html 코드의 용량을 줄이기 위해 압축"""
        code=zlib.compress(code)
        
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

"""파싱한 데이터들을 mongodb에 저장"""
def DBupload(url, engine, keyword):
    url, nowtime, status, server, code, title, lang, textcode = analysis(url)
    
    if status != 'unknown':
        data = {'url':url,'engine':engine,'state':status,'server':server,'keyword':keyword,'title':title,'language':lang,'code':code,'textcode':textcode,'time':nowtime}
        
        mongodb.DB_insert(data)

"""
파싱한 URL들의 데이터를 파싱할 때 속도를 줄이기 위해서 멀티 쓰레드를 사용
멀티 쓰레드의 수는 파싱한 URL들의 개수와 동일함
"""
def ResultToServer(onion_info, word):
    thlist = []
    for onion_url in onion_info.keys():
        onion_engine=onion_info[onion_url]
        th = threading.Thread(target = DBupload, args = (onion_url,onion_engine,word))
        th.setDaemon(True)
        th.start()
        thlist.append(th)

    for thread in thlist:
                thread.join()

"""멀티 프로세스를 사용하기 위해 각 검색 언어 마다 함수로 만들어 검색"""
#영어
def en(key):
    darK_log.Create_log_file()
    for Word in key:
        """
        6개의 카테고리("child_porn", "drug", "counterfeit", "murder", "hack", "weapon")를
        받아 해당 카테고리에 있는 검색어를 하나씩 검색
        """
        for basics in basics_keyword.enC[Word]:
            """basics_parser 함수로 검색을 진행"""
            search_class=dark_Crawler.basics_parser(basics,session)
            dicts={}
            """각 검색 엔진 별로 URL들을 딕셔너리로 저장"""
            ahmiavalue={'ahmia':search_class.ahmia()}
            torSearchvalue={'torSearch':search_class.tor()}
            """Deduplication 함수를 통해 각 검색 엔진에서 중복된 URL들을 체크하여 제거"""
            dicts.update(dark_Crawler.Deduplication(torSearchvalue,ahmiavalue))
            """URL의 데이터 파싱"""
            ResultToServer(dicts, basics)

#한국어
def ko(key):
    darK_log.Create_log_file()
    for Word in key:
        for basics in basics_keyword.koC[Word]:
            search_class=dark_Crawler.basics_parser(basics,session)
            dicts={}
            ahmiavalue={'ahmia':search_class.ahmia()}
            torSearchvalue={'torSearch':search_class.tor()}
            dicts.update(dark_Crawler.Deduplication(torSearchvalue,ahmiavalue))
            ResultToServer(dicts, basics)

#일본어
def ja(key):
    darK_log.Create_log_file()
    for Word in key:
        for basics in basics_keyword.jaC[Word]:
            search_class=dark_Crawler.basics_parser(basics,session)
            dicts={}
            ahmiavalue={'ahmia':search_class.ahmia()}
            torSearchvalue={'torSearch':search_class.tor()}
            dicts.update(dark_Crawler.Deduplication(torSearchvalue,ahmiavalue))
            ResultToServer(dicts, basics)

#중국어
def ch(key):
    darK_log.Create_log_file()
    for Word in key:
        for basics in basics_keyword.chC[Word]:
            search_class=dark_Crawler.basics_parser(basics,session)
            dicts={}
            ahmiavalue={'ahmia':search_class.ahmia()}
            torSearchvalue={'torSearch':search_class.tor()}
            dicts.update(dark_Crawler.Deduplication(torSearchvalue,ahmiavalue))
            ResultToServer(dicts, basics)

#러시아어
def ru(key):
    darK_log.Create_log_file()
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
    
    """시간이 얼마나 걸리는지 체크"""
    print(f'Finished in {round(finish-start, 2)} second(s)')
