"""검색 엔진에 검색 단어를 검색하여 URL들을 파싱하는 모듈"""
from bs4 import BeautifulSoup
import time
import re
import mongodb

start = time.time()  # 시작 시간 저장
#Url REGEX
ANY_URL_REGEX = "^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\W\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"

class basics_parser():
    def __init__(self, basicsword, session):
        self.basic = basicsword
        self.session=session
    
    """ahmia 검색엔진 함수"""
    def ahmia(self):
        url = "https://ahmia.fi/search/?q=" + self.basic
        proxies = {'http': 'socks5h://localhost:9150',
                    'https': 'socks5h://localhost:9150'}
        
        """검색 엔진에 접속이 될때까지 접속을 시도"""
        while(1):
            try:
                origin = self.session.get(url, proxies=proxies, headers={'Connection':'close'})
                origin.close()
                break
            except Exception as e:
                time.sleep(5)
        
        """html 파싱"""
        Soup = BeautifulSoup(origin.text, 'html.parser')
        
        url_box=[]

        """검색 단어를 검색했을 때 아무것도 나오지 않으면 빈 url 리스트를 반환"""
        if Soup.text.find("Sorry, but Ahmia couldn't find results for")>=0:
            return url_box
        """a 태그를 찾고 href 속성에 url만 파싱"""
        for a_tag in Soup.find_all('a', href=True):
            if a_tag["href"].find('url=')>=0:
                url_box.append(a_tag['href'][a_tag["href"].find('url=')+4:])
            else:
                url_box.append(a_tag['href'])
        
        onion_box=[]
        
        """파싱한 url에 .onion이 있는지 확인하여 .onion이 있으면 저장함"""
        for url_one in url_box:
            if re.findall(ANY_URL_REGEX, url_one) != []:
                if url_one.find(".onion")>=0:
                    onion_box.append(url_one)
                    onion_box = list(set(onion_box))
        
        onion_box = list(set(onion_box))
        
        """중복제거 함수"""
        onion_box = mongodb.DB_Compare(onion_box)
        return onion_box
    
    def tor(self):
        url = "http://torchdeedp3i2jigzjdmfpn5ttjhthh5wbmda2rr3jvqjg5p77c54dqd.onion/search?query=" + self.basic
        proxies = {'http': 'socks5h://127.0.0.1:9150',
                    'https': 'socks5h://127.0.0.1:9150'}
        
        while(1):
            try:
                origin = self.session.get(url, proxies=proxies, headers={'Connection':'close'})
                origin.close()
                break
            except Exception as e:
                time.sleep(5)
        
        Soup = BeautifulSoup(origin.text, 'html.parser')
        
        url_box=[]
        
        if Soup.text.find("returned 0 results.")>=0:
            return url_box
        for a_tag in Soup.find_all('a', href=True):
            url_box.append(a_tag['href'])
        
        onion_box=[]
        
        for url_one in url_box:
            if re.findall(ANY_URL_REGEX, url_one) != []:
                if url_one.find(".onion")>=0:
                    onion_box.append(url_one)
                    onion_box = list(set(onion_box))
                    
        onion_box = list(set(onion_box))
        onion_box = mongodb.DB_Compare(onion_box)
        return onion_box

def Deduplication(*args):
        tmpA=list(args)[0]
        tmpB=list(args)[1]

        tmpAstring=list(tmpA.keys())[0]
        tmpBstring=list(tmpB.keys())[0]
        alls={}
        for i in tmpA[tmpAstring]:
            if(tmpB[tmpBstring].count(i)>0):
                tmpB[tmpBstring].remove(i)
                alls.update({i:tmpAstring+' '+tmpBstring})
            else:
                alls.update({i:tmpAstring})

        for j in tmpB[tmpBstring]:
            alls.update({j:tmpBstring})

        return alls