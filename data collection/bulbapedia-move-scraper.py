'''
Scrapes moves for a pokemon from bulbapedia

DOES NOT ALWAYS WORK!
'''

import json
import requests
from bs4 import BeautifulSoup as soup
import re

name = 'Araquanid'

def str_to_num(s):
    isNum = all(['0' <= letter <= '9' for letter in s]) and len(s) > 0 #and ord(letter) != 8212
    return int(s) if isNum else None

url = "https://bulbapedia.bulbagarden.net/wiki/" + name + "_(Pokemon)"
page = requests.get(url)
page_soup = soup(page.text, "html.parser")

#col = list(soup.body.div)[1]
tabs = page_soup.find_all("table", {"class":"roundy"})[2:] #exclude titles
movepools = [list(list(y.find_all("table"))[2]) for y in tabs if y.find("big") and len(list(y.find_all("table"))) == 3] #gets all move tables
moves = {}

#Level up and HMs TMs Table
for pool in movepools[:2]:
    if (len(pool) == 4):
        continue #avoid empty movepools (e.g. breeding set might be empty)
    
    for i in range(3, len(pool), 2):
        cur = list(pool[i])
        print(cur[-11].span.text.strip())
        moves[cur[-11].span.text.strip()] = {
            "Type":     cur[-9].span.text.strip(),
            "Category": cur[-7].span.text.strip(),
            "Power":    str_to_num(cur[-5].span.text.strip()),
            "Accuracy": str_to_num(cur[-3].span.text.strip()[:3]),
            "PP":       int(cur[-1].text.strip())
        } 
        ''' negative indices are used because the front of the 
        table varies, but the tail end is always constant'''

# Tutoring and Breeding Tables
for pool in movepools[2:]:
    if (len(pool) == 4): continue
    for i in range(3, len(pool), 2):
            cur = list(pool[i])
            moves[cur[-11].span.text.strip()] = {
                "Type":     cur[-9].span.text.strip(),
                "Category": cur[-7].text.strip(),
                "Power":    str_to_num(cur[-5].text.strip()),
                "Accuracy": str_to_num(cur[-3].text.strip()[:-1]),#to get rid of the percent sign
                "PP":       cur[-1].text.strip()
            }


