# Data Collection

Competitive data about pokemon and moves were scraped from smogon and bulbapedia and stores as CSVs delimited by semicolons. Pokemon and moves are up to date as of 2018-05-19.

**pokemon-data.csv**:

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
            
Scraped by pokemon-data-to-csv.py from smogon-data.json (which is the HTML from https://www.smogon.com/dex/sm/pokemon/). Moves scraped from https://veekun.com. 
 <br>
 <br>

**move-data-backup.csv**:

	Index - Int
    Name - String
    Type - String
    Category - String
    Contest - String
    PP - Int
    Power - Int or None
    Accuracy - Int or None
    Gen - Int

Scraped by all-moves-scraper.py from https://bulbapedia.bulbagarden.net/wiki/List_of_moves.

