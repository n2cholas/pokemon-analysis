# Smogon Scraper

import json
import requests
from bs4 import BeautifulSoup as soup

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
    Moves - Dictionary of Dictionaries, containing:
        Key:    Name - String
        Value:  Dictionary: 
            Type - String
            Category - String
            Power - Int or None
            Accuracy - Int or None
            PP - Int

'''

# Gets moves and stores it as a dictionary with the move name as the key and values as dictionaries containing details
def get_moves(name):
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
        if (len(pool) == 4): continue #avoid empty movepools (e.g. breeding set might be empty)
        for i in range(3, len(pool), 2):
            cur = list(pool[i])
            moves[cur[-11].span.text.strip()] = {
                "Type":     cur[-9].span.text.strip(),
                "Category": cur[-7].span.text.strip(),
                "Power":    str_to_num(cur[-5].span.text.strip()),
                "Accuracy": str_to_num(cur[-3].span.text.strip()[:3]),
                "PP":       int(cur[-1].text.strip())
            } 
            ''' negative indices are used because the front of the 
            table varies, but the tail end is always constant'''

    return moves

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

pokemon = [] #will be list of pokemon
alternate_forms = ['Arceus', 'Deoxys'] #these pokemon have alterante forms listed in evos

f = open('pokemon-data.csv', 'w')
f.write('Name;Types;Abilities;Tier;HP;Attack;Defense;Special Attack;Special Defense;Speed;Next Evolution(s);Moves\n')

with open('smogon-data.json') as json_data:
    pokemon = json.load(json_data)['pokemon']

for p in pokemon    :
    if p['name'][:6] == 'Arceus' and p['name'] != 'Arceus': 
        continue #so the alternate arceus forms don't get saved
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