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

SCRAPE_LINKS = False
DOWNLOAD_LINKS = True 

input_dir = "/kaggle/input/cifar-10-fake-image-dataset/cifar-10-dataset/" #! Kaggle path
working_dir = "/kaggle/working/" #! Kaggle path

# from distutils.dir_util import copy_tree
# source_dir = "/kaggle/input/spreadthesign-ukrainian-sign-language-videos"
# destination_dir = "/kaggle/working/"
# copy_tree(source_dir, destination_dir)

import csv
import requests
from bs4 import BeautifulSoup
import time
HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

def scrape_website(url, writer):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        src = soup.find('video')['src']
    except TypeError:  
        src = "UNAVAILABLE" 

    text = soup.find('h2').text.strip() if soup.find('h2') else "UNAVAILABLE"

    writer.writerow([text,src])
    
if SCRAPE_LINKS:
    with open('videos.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for i in range(1,4958): 
            print(f"{i} ")
            scrape_website('https://www.spreadthesign.com/uk.ua/word/'+str(i), writer)
        
import urllib.request
import os
import re

if DOWNLOAD_LINKS:
    if not os.path.exists('videos'):
        os.makedirs('videos')
    with open('videos.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        with open('downloads.csv', 'w', newline='', encoding='utf-8') as downloads_file:
            writer = csv.writer(downloads_file)
            
            index = 0
            for row in reader:
                time.sleep(0.3)
                index += 1
                text, src = row
                if src!= "UNAVAILABLE" and text!= "UNAVAILABLE":
                    unsafe_chars = r'[*/\"<>|@`\']'
                    filename = f"videos/{index}__{re.sub(unsafe_chars, '_', text)}"
                    try:
                        urllib.request.urlretrieve(src, filename)
                        print(f"Downloaded {filename}")
                        
                        writer.writerow([text, src, filename])
                        
                    except Exception as e:
                        print(f"Failed to download {filename}: {e}")
                        writer.writerow([text, src, "COULD NOT DOWNLOAD"])
                else:
                    writer.writerow([text, src, "UNAVAILABLE"])
