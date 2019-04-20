# Smogon Scraper

import json
import requests
from bs4 import BeautifulSoup as soup
import re

'''
Notes:
- All mega evolutions, alternate forms, and regional variants
  are considered different pokemon
- Was going to scrape from: https://www.smogon.com/dex/sm/pokemon/, 
  however, ajax requests were too cumbersome. Instead, downloaded
  HTML used json data from HTML file
- Arceus is considered one normal type pokemon (alternate types not listed)

CSV Specification:
    Name - String
    Types - List of Strings
    Abilities - List of Strings
    Tier - String
    HP - Int
    Attack - Int
    Defense - Int
    Special Attack - Int
    Special Defense - Int
    Speed - Int
    Next Evolution(s) - List of Strings
    Moves - List of Strings (of move names)

'''

# Gets moves and stores it as a dictionary with the move name as the key and values as dictionaries containing details
def get_moves(name):
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
        return move_names

    for lst in table[7::2]: #every odd list of the table
        for move in list(lst)[1::2]: #every odd element is a move
            try:
                if move.a['href'][:11] == '/dex/moves/':
                    move_names.append(re.sub('[^0-9a-zA-Z ]+', '\'', move.a.text.strip()))
            except:
                pass

    if move_names == []: 
        print('Warning: empty move list for ' + name)

    return move_names

pokemon = [] #will be list of pokemon
alternate_forms = ['Arceus', 'Deoxys', 'Silvally' ] #these pokemon have alterante forms listed in evos
#,'Giratina','Greninja','Hoopa', 'Kyurem','Landorus','Shaymin','Tornadus','Thundurus']

f = open('pokemon-data.csv', 'w')
f.write('Name;Types;Abilities;Tier;HP;Attack;Defense;Special Attack;Special Defense;Speed;Next Evolution(s);Moves\n')

with open('smogon-data.json') as json_data:
    pokemon = json.load(json_data)['pokemon']

for p in pokemon    :
    if p['name'][:6] == 'Arceus' and p['name'] != 'Arceus': 
        continue #so the alternate arceus forms don't get saved
    elif p['name'][:8] == 'Silvally' and p['name'] != 'Silvally':
        continue
    moves = get_moves(p['name'])

    for form in p['alts']:
        name = p['name'] if form['suffix'] == '' else (p['name'] + '-'+  form['suffix'])
        evolutions = str(p['evos'] if name not in alternate_forms else []) #account for evolutions in alternate forms
        tier = form['formats'][0] if len(form['formats']) > 0 else '' 
        f.write(
            name+';'+
            str(form['types'])+';'+
            str(form['abilities'])+';'+
            tier+';'+
            str(form['hp'])+';'+
            str(form['atk'])+';'+
            str(form['def'])+';'+
            str(form['spa'])+';'+
            str(form['spd'])+';'+
            str(form['spe'])+';'+
            str(evolutions)+';'+
            str(moves)+"\n"         
        )
f.close()
