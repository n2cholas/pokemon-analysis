import requests
from bs4 import BeautifulSoup as soup

def str_to_num(s):
    isNum = all(['0' <= letter <= '9' for letter in s]) and len(s) > 0 #and ord(letter) != 8212
    return int(s) if isNum else None

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
        cur[11].text.strip()+';'+ #pp
        cur[13].text.strip()+';'+ #power
        cur[15].text.strip()+';'+ #accuracy (remove percent symbol)
        cur[17].text.strip()+'\n'
    ).replace("*","")
    f.write(temp_str)

f.close()
