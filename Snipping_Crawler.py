'''
검색에 사용한 검색 엔진
Torch, Ahmia, Onion Index Search Engine
'''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from Screenshot import Screenshot_Clipping
from webdriver_manager.chrome import ChromeDriverManager
import time

tor_proxy = "127.0.0.1:9150" # Tor 브라우저의 프록시 서버

chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors') # SSL(안전하지 않음) 스킵
chrome_options.add_argument('--disable-extensions') # 확장 프로그램 사용안함
chrome_options.add_argument("headless")
# chrome_options.add_argument('--incognito')
# chrome_options.add_argument('--user-data=C:\\Users\\SCHCsRC\\AppData\\Local\\Google\\Chrome\\User Data\\Default') # chrome 프로필을 사용
chrome_options.add_argument('--proxy-server=socks5://%s' % tor_proxy) # 프록시
# driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=chrome_options)

ob=Screenshot_Clipping.Screenshot()
url = "http://torchdeedp3i2jigzjdmfpn5ttjhthh5wbmda2rr3jvqjg5p77c54dqd.onion/"
driver.get(url)
img_url=ob.full_Screenshot(driver, save_path=r'.', image_name='Myimage.png')