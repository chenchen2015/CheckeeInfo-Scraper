# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 18:50:16 2017

@author: Chen Chen

@version: 1.0

@license: MIT License
"""
import urllib
import time
from datetime import datetime
from bs4 import BeautifulSoup

visaURL = 'http://checkee.info/main.php?dispdate={0:04d}-{1:02d}'
tabWidth = 11

# Get current time
timestamp = time.time()
yearNow = datetime.fromtimestamp(timestamp).year
monthNow = datetime.fromtimestamp(timestamp).month
currentTime = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

# File handle
fileCSV = open('VISA-Data-{0}.csv'.format(datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')), 'w', encoding='utf-8')

# Record the overall data
totalEntries = 16480
fileCSV.write('{0},{1}\n'.format('Time Updated', 'Total Entries'))
fileCSV.write('{0},{1}\n\n'.format(currentTime, totalEntries))

# Write table headings
fileCSV.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n'.format(
              'User ID', 
              'User Name', 
              'Visa Type', 
              'Visa Entry', 
              'City', 
              'Major',
              'Visa Status',
              'Check Date',
              'Complete Date',
              'Waiting Days'
              ))

# Main Loop
userID = 0
for yr in range(2009,yearNow+1):
    for mo in range(1,13):
        if yr == yearNow and mo > monthNow:
            break
        
        # Scrape a new page
        visaurl = visaURL.format(yr,mo)
        url = urllib.request.urlopen(visaurl)
        visapage = BeautifulSoup(url.read(), "lxml")
        
        # Get table data, only cleared visa entries will be collected
        tabData = visapage('table')[7]
        # Only get those green fields (completed cases)
        tabEntry = tabData('tr',{'bgcolor':'#00FF00'})
        
        print("Scraping Entry: {0}-{1:02d}, {2} records".format(yr,mo,len(tabEntry)))
        
        for idx in range(len(tabEntry)):
            userName     = tabEntry[idx]('td')[1].text
            visaType     = tabEntry[idx]('td')[2].text
            visaEntry    = tabEntry[idx]('td')[3].text
            city         = tabEntry[idx]('td')[4].text
            major        = tabEntry[idx]('td')[5].text
            status       = tabEntry[idx]('td')[-4].text
            checkDate    = tabEntry[idx]('td')[-3].text
            completeDate = tabEntry[idx]('td')[-2].text
            waitDays     = tabEntry[idx]('td')[-1].text

            #print("UserID: {0:05d}, Visa Type: {1}".format(userID, visaType))
            
            fileCSV.write('{0:05d},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n'.format(
              userID,       # User ID
              userName,     # User Name 
              visaType,     # Visa Type 
              visaEntry,    # Visa Entry 
              city,         # City 
              major,        # Major
              status,       # Visa Status
              checkDate,    # Check Date
              completeDate, # Complete Date
              waitDays      # Waiting Days
              ))
            
            userID += 1

fileCSV.close()
print('All Done!')