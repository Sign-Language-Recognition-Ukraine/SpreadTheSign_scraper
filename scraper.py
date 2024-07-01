#  Copyright 2024 Marko Shevchuk

#  This file is part of SpreadTheSign_scraper on GitHub.

#  SpreadTheSign_scraper is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or 
#  (at your option) any later version.

#  SpreadTheSign_scraper is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#  General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with SpreadTheSign_scraper. If not, see <https://www.gnu.org/licenses/>.

SCRAPE_LINKS = True
DOWNLOAD_LINKS = False 

# from distutils.dir_util import copy_tree
# source_dir = "/kaggle/input/spreadthesign-ukrainian-sign-language-videos"
# destination_dir = "/kaggle/working/"
# copy_tree(source_dir, destination_dir)

# import pandas as pd
# df = pd.read_csv('downloads.csv', header=None)
# df.rename(columns={0: 'word', 1: 'src_link', 2:'subindex', 3:'local_path'}, inplace=True)
# df.to_csv('downloads.csv', index=False) 

import csv
import requests
from bs4 import BeautifulSoup
import time
HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

def scrape_website(urlBase, urlExt, currentIndex, writer, recursive, subIndex): 
    time.sleep(0.1)
    while(True):
        try:
            response = requests.get(urlBase + urlExt + currentIndex, headers=HEADERS) 
            break 
        except requests.exceptions.RequestException as e:
            if isinstance(e, requests.exceptions.ConnectionError):
                print("Connection error occurred.")
                user_input = input("Do you want to retry or skip this attempt? (r/skip): ").lower()
                if user_input == 'skip':
                    print("Stopping the operation.")
                    return
            elif isinstance(e, requests.exceptions.TooManyRedirects):
                print("EXCEEDED MAX REDIRECTS. Ignoring this error.")
                return 

        
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        src = soup.find('video')['src']
    except TypeError:  
        src = "UNAVAILABLE" 

    if recursive:
        try:
            number = 0
            list = soup.find("div", attrs={"class":"col-md-7"}).find_all('a', attrs={"data-replace":"show-result", "class":"js-replace"})
            if len(list) != 0:
                for item in list:
                    scrape_website(urlBase, f"{item['href']}", "", writer, False, number)
                    number += 1
                return
            
        except (TypeError, AttributeError):  
            print("NOT FOUND ")
    

    text = soup.find('h2').text.strip() if soup.find('h2') else "UNAVAILABLE"

    writer.writerow([text,src,subIndex])
    
if SCRAPE_LINKS:
    with open('links.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for i in range(20476,50000): 
            print(f"{i} ")
            scrape_website('https://www.spreadthesign.com','/uk.ua/word/', str(i), writer, True, 0)
        
import urllib.request
import os
import re

if DOWNLOAD_LINKS:
    if not os.path.exists('videos'):
        os.makedirs('videos')
    with open('links.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        with open('downloads.csv', 'w', newline='', encoding='utf-8') as downloads_file:
            writer = csv.writer(downloads_file)
            writer.writerow(['word', 'src_link', 'subindex', 'local_path'])
            index = 0
            for row in reader:
                index += 1
                text, src, subIndex = row
                if src!= "UNAVAILABLE" and text!= "UNAVAILABLE":
                    time.sleep(0.3)
                    unsafe_chars = r'[*\\?/\"<>|@`:\']'
                    filename = f"videos/{index}__{re.sub(unsafe_chars, '_', text)}.mp4"
                    try:
                        urllib.request.urlretrieve(src, filename)
                        print(f"Downloaded {filename}")
                        
                        writer.writerow([text, src, subIndex, filename])
                        
                    except Exception as e:
                        print(f"Failed to download {filename}: {e}")
                        writer.writerow([text, src, subIndex, "COULD NOT DOWNLOAD"])
                else:
                    writer.writerow([text, src, subIndex, "UNAVAILABLE"])
