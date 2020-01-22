#!/usr/bin/env python
# coding: utf-8

# In[88]:


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 17:26:20 2019
"""


import requests
import bs4
from datetime import datetime
import re
import os
#import urllib
#import urllib2
#from bs4 import BeautifulSoup
from selenium import webdriver
import time
import numpy as np
import pandas as pd

#from pandas import Series, DataFrame

initialpage = 'https://www.boxofficemojo.com/yearly/chart/?yr=2017&p=.htm'
res = requests.get(initialpage, timeout=None)
soup = bs4.BeautifulSoup(res.text, 'html.parser')
#print(soup)



pages = []

for a in soup.find_all('a', href=True):
    if('/release/rl' in a['href']):
        pages.append("https://www.boxofficemojo.com" + a['href'])
       
movieName = []   
domesticGross = []
internationalGross = []
worldwideGross = []
openingWeekendGross = []
runTime = []
genre = []
numTheaters = []
inRelease = []
distributor = []
releaseDates = []
i=0
#for i in range(len(pages)):
for i in range(1):
    
    #This block finds the domestic, international, worldwide and opening weekend grosses askitom
    res = requests.get(pages[0], timeout=None)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    s = soup.find_all("span", class_="money")
 
    
       
    domesticGross.append(str(s[0])[20:-7])
    internationalGross.append(str(s[1])[20:-7])
    worldwideGross.append(str(s[2])[20:-7])
    openingWeekendGross.append(str(s[3])[20:-7])
    
    s = soup.find_all("h1", class_="a-size-extra-large")
    for j in s:
        j = str(j)
        movieName.append(j[31:-5])
        
   
    #This block finds the runtime babyto
    s = soup.find_all("div", class_="a-section a-spacing-none")
    for j in s:
        j = str(j)
        if ' hr ' in j:
            runTime.append(j[64:-13])
    
    #This block finds the genres. If multiple genres are present, they are separated with double space in the array
    
    for j in s:
        j = str(j)
        if 'Genres' in j:  
            j=j[63:-13]
            for p in j:
                if p.isalpha():
                    genre.append(p)
                if "\n" in p:
                    genre.append(" ")
            
                    
              
                    
    #Finds number of theaters the movie is exhibited       
    l=0
    for j in s:
        j = str(j)
        if ' theaters' in j:
            if l== 1:
                numTheaters.append(j[71:-21])
            l += 1
    
    #Finds the "In Release" duration
    for j in s:
        j = str(j)
        if 'In Release' in j:  
            inRelease.append(j[67:-13])
            
    #Finds the distributor of the movie
    for j in s:
        j = str(j)
        if 'Distributor' in j:  
            distributor.append(j[68:-804])
    
    #Finds the release date
    for j in s:
        j = str(j)
        if 'Release Date' in j:
            j = j[133:-124] + " to " + j[240:-17]
            releaseDates.append(j)
            
    rows = zip(movieName,domesticGross,internationalGross,worldwideGross,openingWeekendGross, runTime, genre, numTheaters,inRelease,distributor,releaseDates)     
    import csv

    with open("/Users/Gokce/Desktop/movie_info", "w") as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)
            
            
    path = os.getcwd()  
    path = path + '/movie_pictures'
    path = '/Users/Gokce/Desktop/movie_pictures'
    os.makedirs(path)
    os.chdir(path)
    print(path)
    import io
    from PIL import Image
    import hashlib
    
    def persist_image(folder_path:str,url:str):
        try:
            image_content = requests.get(url).content

        except Exception as e:
            print(f"ERROR - Could not download {url} - {e}")

        try:
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert('RGB')
            file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
            with open(file_path, 'wb') as f:
                image.save(f, "JPEG", quality=85)
            print(f"SUCCESS - saved {url} - as {file_path}")
        except Exception as e:
            print(f"ERROR - Could not save {url} - {e}")
    
    l=0
    s = soup.find_all("img")        
    for j in s:
        if(l==1):
            j = str(j)
            j = j[26:-146]
            persist_image(path, j)
        l += 1     
            


# 
