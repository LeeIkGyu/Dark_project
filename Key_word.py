import requests
import json

def get_word(word):
    url = "https://relatedwords.org/api/related?term=" + word
    res = requests.get(url)

    release = res.json()

    val = []
    
    for i in release:
        if i['score'] is None:
            continue
        elif i['score']>=0.5:
            val.append(i['word'])
    
    return val

category = ["child porn", "hosting", "bitcoin", "drug", "counterfeit", "murder", "hack", "weapon", "porno"]
category_word = {}

for item in category:
    category_word[item] = get_word(item)