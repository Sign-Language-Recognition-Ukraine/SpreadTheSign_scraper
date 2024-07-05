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
DOWNLOAD_LINKS = False 
REDOWNLOAD_LINKS = False 
VALIDATE_DOWNLOADS = False
RENAME_DOWNLOADS = True
# from distutils.dir_util import copy_tree
# source_dir = "/kaggle/input/spreadthesign-ukrainian-sign-language-videos"
# destination_dir = "/kaggle/working/"
# copy_tree(source_dir, destination_dir)

# with open('links.csv', 'r', encoding='utf-8') as f1, open('links_concatenate.csv', 'r', encoding='utf-8') as f2:
#     with open('links_total.csv', 'w', encoding='utf-8') as f_total:
#         f_total.write(f1.read())
#         f_total.write(f2.read())

import csv
import requests
from bs4 import BeautifulSoup
import time
HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

def scrape_website(urlBase, urlExt, currentIndex, writer, recursive, subindex, csvIndex): 
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
                    scrape_website(urlBase, f"{item['href']}", "", writer, False, number, csvIndex)
                    number += 1
                return
            
        except (TypeError, AttributeError):  
            print("NOT FOUND ")
    

    text = soup.find('h2').text.strip() if soup.find('h2') else "UNAVAILABLE"

    writer.writerow([csvIndex,text,src,subindex])

languages = {
            'ar_sy':'/ar.sy/', 'bg_bg':'/bg.bg/', 'zh_hans_cn':'/zh.hans.cn/', 'hr_hr':'/hr.hr/', 
            'cs_cz':'/cs.cz/', 'da_dk':'/da.dk/', 'en_au':'/en.au/', 'en_in':'/en.in/',
            'en_nz':'/en.nz/', 'en_gb':'/en.gb/', 'en_us':'/en.us/', 'et_ee':'/et.ee/',
            'fi_fi':'/fi.fi/', 'fr_fr':'/fr.fr/', 'de_at':'/de.at/', 'de_de':'/de.de/', 
            'el_cy':'/el.cy/', 'el_gr':'/el.gr/', 'hi_in':'/hi.in/', 'is_is':'/is.is/', 
            'isl_intl':'/isl.intl/', 'it_it':'/it.it/', 'ja_jp':'/ja.jp/', 'lv_lv':'/lv.lv/', 
            'lt_lt':'/lt.lt/', 'fa_ir':'/fa.ir/', 'pl_pl':'/pl.pl/', 'pt_br':'/pt.br/',
            'pt_pt':'/pt.pt/', 'ro_ro':'/ro.ro/', 'sk_sk':'/sk.sk/', 'es_ar':'/es.ar/', 
            'es_cl':'/es.cl/', 'es_cu':'/es.cu/', 'es_mx':'/es.mx/', 'es_es':'/es.es/',  
            'sv_se':'/sv.se/', 'tr_tr':'/tr.tr/', 'uk_ua':'/uk.ua/', 'ur_pk':'/ur.pk/', 
            }
language = 'uk_ua'
language_path = languages[language]
if SCRAPE_LINKS:
    with open('links.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for i in range(0,75000): # min 1, max 75000
            print(f"{i} ")
            scrape_website('https://www.spreadthesign.com',f'{language_path}word/', str(i), writer, True, 0, str(i))
        

import urllib.request
import os
import re

skip = -1
if DOWNLOAD_LINKS:
    if not os.path.exists('videos'):
        os.makedirs('videos')
    with open('links.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        with open('downloads.csv', 'a', newline='', encoding='utf-8') as downloads_file:
            writer = csv.writer(downloads_file)
            # writer.writerow(['index', 'word', 'src_link', 'subindex', 'local_path'])
            index = 0
            for row in reader: 
                index += 1 
                id, text, src, subindex = row
                if src!= "UNAVAILABLE" and text!= "UNAVAILABLE":
                    time.sleep(0.33)
                    unsafe_chars = r'[*\\?/\"<>|@`:\';$%^&~`\[\]]'
                    filename = f"videos/{id}_{subindex}_{re.sub(unsafe_chars, '_', text)}.mp4"
                    try:
                        urllib.request.urlretrieve(src, filename)
                        print(f"{index} Downloaded {filename}")
                        
                        writer.writerow([id, text, src, subindex, filename])
                        
                    except Exception as e:
                        print(f"{index} FAILED TO DOWNLOAD {filename}: {e}")
                        writer.writerow([id, text, src, subindex, "COULD NOT DOWNLOAD"])
                else:
                    if src != "UNAVAILABLE":
                        print(f"{index} ANOMALY")
                        writer.writerow([id, text, src, subindex, "ANOMALY"])
                    else: 
                        print(f"{index} SKIPPING")
if REDOWNLOAD_LINKS:
    if not os.path.exists('videos'):
        os.makedirs('videos')
    with open('downloads.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        with open('redownloads.csv', 'w', newline='', encoding='utf-8') as downloads_file:
            writer = csv.writer(downloads_file)
            # writer.writerow(['index', 'word', 'src_link', 'subindex', 'local_path'])
            index = 0
            for row in reader: 
                index += 1 
                id, text, src, subindex, local_path = row
                cnd = local_path == "COULD NOT DOWNLOAD"
                missing = not os.path.exists(local_path) 
                if cnd or missing:
                    time.sleep(0.4)
                    unsafe_chars = r'[*\\?/\"<>|@`:\';$%^&~`\[\]]'
                    filename = f"videos/{id}_{subindex}_{re.sub(unsafe_chars, '_', text)}.mp4"
                    try:
                        urllib.request.urlretrieve(src, filename)
                        print(f"{index} Downloaded {filename}")
                        print(f"CND {cnd} MISSING {missing}")
                        writer.writerow([id, text, src, subindex, filename])
                        
                    except Exception as e:
                        print(f"{index} FAILED TO DOWNLOAD {filename}: {e}")
                        writer.writerow([id, text, src, subindex, "COULD NOT DOWNLOAD"])
                else:
                    writer.writerow([id, text, src, subindex, local_path])
if VALIDATE_DOWNLOADS:
    if not os.path.exists('videos'):
        os.makedirs('videos')
    with open('links.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        with open('downloads.csv', 'r', newline='', encoding='utf-8') as download_file:
            download_reader = csv.reader(download_file)
            with open('valid_downloads.csv', 'w', newline='', encoding='utf-8') as valid_download_file:
                writer = csv.writer(valid_download_file)
                # writer.writerow(['index', 'word', 'src_link', 'subindex', 'local_path'])
                index = 0
                for row in download_reader: 
                    download_id, download_text, download_src, download_subindex, download_local_path = row
                    while True:
                        current = reader.__next__()
                        current_id = current[0]
                        current_text = current[1]
                        current_src = current[2]
                        current_subindex = current[3]
                        if (current_id != download_id):
                            if (current_src != "UNAVAILABLE"):
                                time.sleep(0.33)
                                unsafe_chars = r'[*\\?/\"<>|@`:\';$%^&~`\[\]]'
                                filename = f"videos/{current_id}_{current_subindex}_{re.sub(unsafe_chars, '_', current_text)}.mp4"
                                try:
                                    urllib.request.urlretrieve(current_src, filename)
                                    print(f"{current_id} Downloaded {filename}")
                                    
                                    writer.writerow([current_id, current_text, current_src, current_subindex, filename])
                                    
                                except Exception as e:
                                    print(f"{current_id} FAILED TO DOWNLOAD {filename}: {e}")
                                    writer.writerow([current_id, current_text, current_src, current_subindex, "COULD NOT DOWNLOAD"])
                        else: 
                            writer.writerow([download_id, download_text, download_src, download_subindex, download_local_path])
                            break
if RENAME_DOWNLOADS:
    with open("downloads.csv", mode='r', newline='', encoding='utf-8') as infile, \
            open("clean_downloads.csv", mode='w', newline='', encoding='utf-8') as outfile:
            unsafe_chars = r'[*\\?/\"<>|@`:\';$%^&~`\[\]]'
            input_reader = csv.reader(infile)
            output_writer = csv.writer(outfile)
            
            for row in input_reader:
                id_, word, src_link, subindex, local_path = row
                old_file_path = local_path
                if os.path.exists(local_path):
                    new_file_name = f"{id_}_{subindex}_{re.sub(unsafe_chars, '_', word)}.mp4"
                    new_file_path = f"videos/{new_file_name}"
                    os.rename(old_file_path, new_file_path)
                    
                    row[-1] = str(new_file_path) 
                else: 
                    print(f"{id_} {local_path} DOES NOT EXIST")

                output_writer.writerow(row)
                
