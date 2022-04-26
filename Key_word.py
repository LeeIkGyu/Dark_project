import requests
import json
from translation_key_word import get_translate

def get_word(word):
    url = "https://relatedwords.org/api/related?term=" + word
    res = requests.get(url)

    release = res.json()

    val = []
    
    # score 기반으로 단어를 추출   
    for i in release:
        if i['score'] is None:
            continue
        elif i['score']>=0.5:
            val.append(i['word'])
    
    return val

# 기본 단어
category = ["child porn", "hosting", "bitcoin", "drug", "counterfeit", "murder", "hack", "weapon", "porno"]
category_word = {}

for item in category:
    category_word[item] = get_word(item)
    
# 번역할 언어
# 한국어, 일본어, 중국어(간체), 러시아어
lang = ["ko", "ja", "zh-CN", "ru"]

for i, j in zip(category, lang):
    get_translate(category_word[i], j)