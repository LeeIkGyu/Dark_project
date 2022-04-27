from bs4 import BeautifulSoup
import requests
import time

class basics_parser():
    def __init__(self, basicsword):
        self.basic = basicsword
    
    def tor(self):
        