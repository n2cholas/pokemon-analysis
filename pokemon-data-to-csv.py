# Smogon Scraper
'''
Notes:
- All mega evolutions, alternate forms, and regional variants
  are considered different pokemon
- Was goingt o scrape from: https://www.smogon.com/dex/sm/pokemon/, 
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
    Moves - Set of Dictionaries, containing:
        Name - String
        Type - String
        Category - String
        Power - Int or NaN
        Accuracy - Int or NaN
        PP - Int
        Description - String

'''

import json

pokemon = [] #will be list of pokemon
alternate_forms = ['Arceus', 'Deoxys'] #these pokemon have alterante forms listed in evos

f = open('pokemon-data.csv', 'w')
f.write('Name; Types; Abilities; Tier; HP; Attack; Defense; Special Attack; Special Defense; Speed; Next Evolution(s); Moves\n')

with open('smogon-data.json') as json_data:
    pokemon = json.load(json_data)['pokemon']

for p in pokemon:
    if p['name'][:6] == 'Arceus' and p['name'] != 'Arceus':
        continue
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
            str(evolutions)+"\n"         
        )
f.close()