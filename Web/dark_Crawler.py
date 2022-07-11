"""예외 및 오류를 기록하는 모듈"""
from logging.config import dictConfig
from pytz import timezone
from datetime import datetime
import logging
import os

fmt = "%Y_%m_%d"

nowtime = datetime.now(timezone('Asia/Seoul')).strftime(fmt)

dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s %(message)s',
        }
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': r'C:\Users\SCHCsRC\Desktop\Code\Python\Project\log_{0}.log'.format(nowtime),
            'formatter': 'default',
            'encoding' : 'utf-8'
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file']
    }
})

"""시스템 시간에 맞게 log 파일을 생성하는 함수"""
def Create_log_file():
    if not os.path.isfile(r'C:\Users\SCHCsRC\Desktop\Code\Python\Project\log_{0}.log'.format(nowtime)):
        file = open(r'C:\Users\SCHCsRC\Desktop\Code\Python\Project\log_{0}.log'.format(nowtime), 'r', encoding='utf-8')
        file.close()

# def log_info(message):
#     logging.info(message)

"""오류 및 예외를 기록"""
def log_error(message):
    logging.error(message)
