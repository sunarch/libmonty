#!/usr/bin/env python3

import logging
import requests
import time

HOST = input().strip()
INTERVAL = 30

# create logger
logger = logging.getLogger('uptest_logger')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch1 = logging.StreamHandler()
ch1.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch2 = logging.FileHandler('uptest.log', encoding='UTF-8')
ch2.setLevel(logging.DEBUG)

# create formatter
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# add formatter to ch
ch1.setFormatter(formatter)
ch2.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch1)
logger.addHandler(ch2)

# loop test until interrupted

while True:
    
    try:
        r = requests.head(f'http://{HOST}')
        logger.info('HTTP:  %s %s', r.status_code, r.reason)
        rs = requests.head(f'https://{HOST}')
        logger.info('HTTPS: %s %s', rs.status_code, rs.reason)
        time.sleep(INTERVAL)
    except KeyboardInterrupt:
        break
