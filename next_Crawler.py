from bs4 import BeautifulSoup
import requests
import time
import re
import dark_Crawler
import basics_category
from pytz import timezone
from datetime import datetime

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
    category = ""
    lang = ""
    nowtime = datetime.now(timezone('Asia/Seoul')).srtftime(fmt)[:9]
    
    try:
        res = session.get(url, timeout=10, headers={"Connection" : "close"})
        status = res.status_code
        requests_txt = res.text
        
        Soup = BeautifulSoup(requests_txt, "html.parser")
        
        title, lang = info_return(Soup)
        
        category = category_return(lang, title)
        
        if category == "unknown":
            category = category_return(lang, requests_txt)
        
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
                    onion_box.append(url_one[:url_one.find('.onion')+6])