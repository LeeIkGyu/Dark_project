from attr import s
from pymongo import MongoClient
import traceback ## error 위치(정보) 표시하기 위해 사용 
import darK_log
import threading
import main_Crawler

client = MongoClient(connect = False, host = 'localhost', port = 27017)

def DB_insert(data): ## 데이터 추가, 삭제 및 변경 동작
        try:
            DWdb = client['DWMongodb'] ## db name
            # print('MongoDB - DWMongodb Connected Success') # 클라이언트(데베) 연결 성공 
            #데이터 입 
            CrawlingData = {
                'URL' : data.get('url'),
                'Engine' : data.get('engine'),
                'State' : data.get('state'),
                'Server' : data.get('server'),
                'Keyword' : data.get('keyword'),
                'Title' : data.get('title'),
                'Language' : data.get('language'),
                'Code' : data.get('code'),
                'Textcode' : data.get('textcode'),
                'Time' : data.get('time')
            }
            
            CrawlingInfo_live = DWdb["CrawlingInfo_live"] # 실시간 데이터 들어갈 곳 
            DWdb_Data = DWdb.CrawlingInfo_live.update_one({'URL': data.get('url')},  {"$set": CrawlingData}, upsert=True) #데이터 삽입 
            # print('Data Insert Success')           

        except:
            darK_log.log_error(traceback.format_exc())

def DB_Url_insert(value, url_data):
    try:
        DWdb_url = client['DWMongodb_url']
        # print('MongoDB - DWMongodb_url Connected Success')

        CrawlingUrlData ={
            'Category' : value,
            'URL' : url_data
        }

        CrawlingInfo_URL = DWdb_url["CrawlingInfo_URL"]

        DWMongodb_url = DWdb_url.CrawlingInfo_URL.update_one({'Category': value, 'URL' : url_data},  {"$set": CrawlingUrlData}, upsert=True)
        # print('URL Data Insert Success')
    
    except:
        darK_log.log_error(traceback.format_exc())

# def DB_Compare(urls):
#     lock = threading.Lock()
#     lock.acquire()
#     try:
#         for url in urls:
#             if url in main_Crawler.onion_df:
#                 urls.remove(url)
#         main_Crawler.onion_df.append(urls)
#         return urls
#     finally:
#         lock.release()