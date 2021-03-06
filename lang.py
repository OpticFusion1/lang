#!#/usr/bin/env python3
# Quick way to scrape merriam-webster's dictionary and thesaurus
#
# Author: Optic_Fusion1
# Date: 3/05/2022

import requests
import argparse
from bs4 import BeautifulSoup
from string import ascii_lowercase
from pathlib import Path

version = "0.3.0";

print(f"Running lang {version}")

def processUrl(base_url, file_name):
    file_path = Path(file_name);

    if file_path.exists():
        file = open(file_name, 'a', encoding='utf-8');
    else:
        file = open(file_name, 'w', encoding='utf-8');

    r = requests.get(base_url, headers={'user-agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(r.content, 'html5lib')
    inputTags = soup.findAll(attrs={"aria-label" : "Last"})
    last_page = inputTags[0]['data-page']

    for c in ascii_lowercase + '0':
        url = base_url + str(c) + '/'
        print(f"Scraping {url}");
        r = requests.get(url, headers={'user-agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(r.content, 'html5lib')
        inputTags = soup.findAll(attrs={"aria-label" : "Last"})
        last_page = inputTags[0]['data-page']
        if last_page:
            for x in range (1, int(last_page) + 1):
                final_url = url + str(x);
                r = requests.get(final_url, headers={'user-agent': 'Mozilla/5.0'})
                soup = BeautifulSoup(r.content, 'html5lib')
                for foo in soup.findAll('a'):
                    try:
                        clazz = foo['class']
                        if clazz[0] == 'pb-4' and clazz[1] == 'pr-4' and clazz[2] == 'd-block':
                            text = foo.text
                            print(text)
                            file.write(text + "\n")
                    except:
                        continue
        else:
            final_url = url + str(x);
            r = requests.get(final_url, headers={'user-agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(r.content, 'html5lib')
            for foo in soup.findAll('a'):
                try:
                    clazz = foo['class']
                    if clazz[0] == 'pb-4' and clazz[1] == 'pr-4' and clazz[2] == 'd-block':
                        text = foo.text
                        print(text)
                        file.write(text + "\n")
                except:
                    continue
        
    file.close();

processUrl('https://www.merriam-webster.com/browse/dictionary/', 'Base-Dictionary.txt');
processUrl('https://www.merriam-webster.com/browse/thesaurus/', 'Base-Theasaurus.txt');
