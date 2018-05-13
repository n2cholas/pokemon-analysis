import requests
from bs4 import BeautifulSoup as soup

'''
Scraped from: https://bulbapedia.bulbagarden.net/wiki/List_of_moves

CSV Specification:
    Index - Int
    Name - String
    Type - String
    Category - String
    Contest - String
    PP - Int
    Power - Int or None
    Accuracy - Int or None
    Gen - Int
'''

def str_to_num(s):
    if s[-1] == "*" or s[-1] == "%":
        s = s[:-1]
    isNum = all(['0' <= letter <= '9' for letter in s]) and len(s) > 0 #and ord(letter) != 8212
    return str(int(s)) if isNum else 'None' #turned into string to make writing to csv easier

generation = {"I":1, "II":2, "III":3,"IV":4, "V":5, "VI":6, "VII":7}

url = "https://bulbapedia.bulbagarden.net/wiki/List_of_moves"
page = requests.get(url)
page_soup = soup(page.text, "html.parser")

table = list(page_soup.find("table", {"border":1}))

f = open('move-data.csv', 'w')
f.write('Index;Name;Type;Category;Contest;PP;Power;Accuracy;Gen\n')

for i in range(3, len(table), 2):
    cur = list(table[i])
    temp_str = (
        str(cur[1].text.strip())+';'+ #index i.e. primary key
        cur[3].a.text.strip()+';'+ #name 
        cur[5].span.text.strip()+';'+ #type
        cur[7].span.text.strip()+';'+ #category
        cur[9].span.text.strip()+';'+ #contest
        str_to_num(cur[11].text.strip())+';'+ #pp
        str_to_num(cur[13].text.strip())+';'+ #power
        str_to_num(cur[15].text.strip())+';'+ #accuracy
        str(generation[cur[17].text.strip().replace("*","")])+'\n'
    ).replace("*","")
    f.write(temp_str)

f.close()
