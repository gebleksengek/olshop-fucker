# -*- coding: utf-8 -*-
"""
    Coder: indryanto
"""

import os
from datetime import datetime
import csv

def write(message, messageType=None):
    if messageType == 'exit':
        exit(message)
    elif messageType == 'noLine':
        print(message, end='\r')
    else:
        print(message)

def writeToCsv(username, datas, headers, shopType):
    print('zxcvxv')
    filename = username + str(datetime.now()).replace('-', '').replace(' ', '').replace(':', '').replace('.', '')
    print(filename)
    if shopType == 'shopee':
        outDir = 'outputs/shopee/'
        if not os.path.exists(outDir):
            os.mkdir(outDir)
        with open(outDir + filename, 'w') as csvFile:
            writer = csv.DictWriter(csvFile, headers)
            writer.writeheader()
            for data in datas:
                writer.writerow(data)
        csvFile.close()
    elif shopType == 'bukalapak':
        print(shopType)