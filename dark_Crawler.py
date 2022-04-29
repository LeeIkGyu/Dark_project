from bs4 import BeautifulSoup
import requests
import time
import re

#Url REGEX
ANY_URL_REGEX = "^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\W\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"

class basics_parser():
    def __init__(self, basicsword, session):
        self.basic = basicsword
        self.session=session
    
    def ahmia(self):
        url = "https://ahmia.fi/search/?q=" + self.basic
        proxies = {'http': 'socks5h://localhost:9150',
                    'https': 'socks5h://localhost:9150'}
        
        while(1):
            try:
                origin = self.session.get(url, proxies=proxies, headers={'Connection':'close'})
                origin.close()
                break
            except Exception as e:
                time.sleep(5)
        
        Soup = BeautifulSoup(origin.text, 'html.parser')
        
        url_box=[]
        
        if Soup.text.find("Sorry, but Ahmia couldn't find results for")>=0:
            return "unknown"
        for a_tag in Soup.find_all('a', href=True):
            if a_tag["href"].find('url=')>=0:
                url_box.append(a_tag['href'][a_tag["href"].find('url=')+4:])
            else:
                url_box.append(a_tag['href'])
        
        onion_box=[]
        
        for url_one in url_box:
            if re.findall(ANY_URL_REGEX, url_one) != []:
                if url_one.find(".onion")>=0:
                    onion_box.append(url_one)
                    onion_box = list(set(onion_box))
                    
        onion_box = list(set(onion_box))
        return onion_box, self.basic, "https://ahmia.fi/"
    
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
            return "unknown"
        for a_tag in Soup.find_all('a', href=True):
            url_box.append(a_tag['href'])
        
        onion_box=[]
        
        for url_one in url_box:
            if re.findall(ANY_URL_REGEX, url_one) != []:
                if url_one.find(".onion")>=0:
                    onion_box.append(url_one)
                    onion_box = list(set(onion_box))
                    
        onion_box = list(set(onion_box))
        return onion_box, self.basic, "http://torchdeedp3i2jigzjdmfpn5ttjhthh5wbmda2rr3jvqjg5p77c54dqd.onion/"