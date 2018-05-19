'''
Scrapes move names for a pokemon from Veekun (used in pokemon-data-to-csv)
'''

import json
import requests
from bs4 import BeautifulSoup as soup
import re

name = 'Zygarde-10%'

name = name.lower().replace('%', '')
pos = name.find('-')
space = name.rfind(' ')
suffix = name[pos+1:space if space != -1 else len(name)].replace('\'','')

# deals with pokemon with alternate male/female forms
if suffix == 'm': 
    suffix = 'male'
elif suffix == 'f': 
    suffix = 'female'

#deals with other forms (alola, therian, etc)
if name == 'nidoran-m': 
    name = 'nidoran♂'
elif name == 'nidoran-f': 
    name = 'nidoran♀'
elif name == 'flabebe': 
    name = 'flabébé'
elif name == 'farfetch\'d':
    name = 'farfetch’d'
elif pos != -1 and name not in ['ho-oh', 'porygon-z', 'jangmo-o', 'kommo-o', 'hakamo-o']:
    name = name[:pos] + '?form=' + suffix

url = "https://veekun.com/dex/pokemon/" + name 
page = requests.get(url)
page_soup = soup(page.text, "html.parser")
move_names = []

try:
    table = list(page_soup.find("table", {"class":"dex-pokemon-moves dex-pokemon-pokemon-moves striped-rows"})) #big table with all moves
    levelup_lst = list(table[7]) #everything before 7 are headers
    #levelup_lst[odd numbers].a are the move names as URLs
    #for moves, the href looks like: href="/dex/moves/<move name>"
except TypeError:
    print('Could not get table for ' + name)

for lst in table[7::2]: #every odd list of the table
    for move in list(lst)[1::2]: #every odd element is a move
        try:
            if move.a['href'][:11] == '/dex/moves/':
                move_names.append(re.sub('[^0-9a-zA-Z ]+', '\'', move.a.text.strip()))
        except:
            pass

if move_names == []: 
    print('Warning: empty move list for ' + name)

print(move_names)