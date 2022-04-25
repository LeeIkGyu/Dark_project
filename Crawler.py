'''
검색에 사용한 검색 엔진
Torch, Ahmia, Onion Index Search Engine
'''

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

tor_proxy = "127.0.0.1:9150" # Tor 브라우저의 프록시 서버

os.popen(r"C:\Users\SCHCsRC\Desktop\Tor Browser\Browser\firefox.exe") # Tor 브라우저 실행
time.sleep(5)

chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors') # SSL(안전하지 않음) 스킵
chrome_options.add_argument('--disable-extensions') # 확장 프로그램 사용안함
chrome_options.add_argument("--incognito") # 시크릿 모드로 실행
chrome_options.add_argument('--user-data=C:\\Users\\SCHCsRC\\AppData\\Local\\Google\\Chrome\\User Data\\Default') # chrome 프로필을 사용
chrome_options.add_argument('--proxy-server=socks5://%s' % tor_proxy) # 프록시
driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)

