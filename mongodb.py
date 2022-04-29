from pymongo import MongoClient
import traceback ## error 위치(정보) 표시하기 위해 사용 

def main(): ## 데이터 추가, 삭제 및 변경 동작 
    DWdb = client['DWMongodb'] ## db name     
    print('MongoDB - DWMongodb Connected Success')



    # 데이터 입력 시험 
    CrawlingData = {
        'URL' : 'https://www.naver.com',
        'Category' : '포르노',
        'Bitcoin_Address' : 'addddddd'
    }

    CrawlingInfo_live = DWdb["CrawlingInfo_live"] # 실시간 데이터 들어갈 곳
    CrawlingInfo_add = DWdb["CrawlingInfo_add"] #  초기에 정한 카테고리 이외의 데이터 

    DWdb_Data = DWdb.CrawlingInfo_live.insert_one(CrawlingData) #데이터 삽입 

    print('데이터 입력 성공')


try : 
    client = MongoClient(host = 'localhost', port = 27017) 
    main()
except :
    print('오류 발생.')
    print(traceback.format_exc())
