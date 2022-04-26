'''
    영어, 한국어, 일어, 중국어, 러시아어
'''

import requests

# 파파고 API에서 발급하는 ID와 Secret 값
client_id = "ziqm0KurlfFs1S672BMv"
client_secret = "8MU4sfIFD6"

def get_translate(text, lan):
    data = {
        'text' : text,
        'source' : lan,
        'target' : 'en'
    }
    
    # 파파고 API 사용
    url = "https://openapi.naver.com/v1/papago/n2mt"
    
    header = {"X-Naver-Client-Id" : client_id,
                "X-Naver-Client-Secret" : client_secret}
    
    response = requests.post(url, headers=header, data=data)
    rescode = response.status_code
    
    if rescode == 200:
        t_data = response.json()
        print(t_data['message']['result']['translatedText'])
    else:
        print("Error Code:", rescode)