from logging.config import dictConfig
from pytz import timezone
from datetime import datetime
import logging

fmt = "%Y-%m-%d"

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
            'filename': r'C:\Users\SCHCsRC\Desktop\코딩\파이썬\Project\log_{0}.log'.format(nowtime),
            'formatter': 'default',
            'encoding' : 'utf-8'
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file']
    }
})

def log_info(message):
    logging.info(message)
    
def log_error(message):
    logging.error(message)