# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 18:50:16 2017

@author: Chen Chen

@version: 1.2

@license: MIT License
"""
import urllib.request
import time
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

visaURL = 'https://www.checkee.info/main.php?dispdate={0:04d}-{1:02d}'

# Get current time
timestamp = time.time()
yearNow = datetime.fromtimestamp(timestamp).year
monthNow = datetime.fromtimestamp(timestamp).month
currentTime = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

# File handle
time_string = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
filename = f'VISA-Data-{time_string}.csv'

# Initialize dataframe
df = pd.DataFrame(
    columns=[
        'UserName',
        'VisaType',
        'VisaEntry',
        'City',
        'Major',
        'VisaStatus',
        'CheckDate',
        'CompleteDate',
        'WaitDays'
    ]
)
# set column datatypes
df['UserName'] = pd.Series([], dtype=np.str)
df['VisaType'] = pd.Categorical([])
df['VisaEntry'] = pd.Categorical([])
df['Major'] = pd.Categorical([])
df['VisaStatus'] = pd.Categorical([])
df['City'] = pd.Categorical([])
df['CheckDate'] = pd.Series([], dtype='datetime64[ns]')
df['CompleteDate'] = pd.Series([], dtype='datetime64[ns]')
df['WaitDays'] = pd.Series([], dtype=np.int8)

# Main Loop
for yr in range(2009,yearNow+1):
    for mo in range(1,13):
        if yr == yearNow and mo > monthNow:
            break
        # Scrape a new page
        visaurl = visaURL.format(yr,mo)
        req = urllib.request.Request(visaurl, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read()
        visapage = BeautifulSoup(html, 'html5lib')
        # Only get the completed cases - those marked in green
        tabEntry = visapage.find_all('tr', attrs={'bgcolor':'#4CBB17'})
        print("Scraping Entry: {0}-{1:02d}, {2} records".format(yr,mo,len(tabEntry)))

        for idx in range(len(tabEntry)):
            userName     = tabEntry[idx]('td')[1].text.replace(',','')
            visaType     = tabEntry[idx]('td')[2].text.replace(',','')
            visaEntry    = tabEntry[idx]('td')[3].text.replace(',','')
            city         = tabEntry[idx]('td')[4].text.replace(',','')
            major        = tabEntry[idx]('td')[5].text.replace(',','')
            status       = tabEntry[idx]('td')[-5].text.replace(',','')
            checkDate    = tabEntry[idx]('td')[-4].text.replace(',','')
            completeDate = tabEntry[idx]('td')[-3].text.replace(',','')
            waitDays     = tabEntry[idx]('td')[-2].text.replace(',','')
            #print("caseID: {0:05d}, Visa Type: {1}".format(caseID, visaType))
            df = df.append(
                {
                    'UserID'       : caseID,
                    'UserName'     : userName,
                    'VisaType'     : visaType,
                    'VisaEntry'    : visaEntry,
                    'City'         : city,
                    'Major'        : major,
                    'VisaStatus'   : status,
                    'CheckDate'    : checkDate,
                    'CompleteDate' : completeDate,
                    'WaitDays'     : waitDays
                },
                ignore_index=True
            )
            caseID += 1
            
df.to_csv(filename)
print('All Done!')