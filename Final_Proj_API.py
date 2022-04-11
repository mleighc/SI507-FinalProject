import requests
import csv
import xmltodict, json

#READ IN A CSV WITH GAME ATTRIBUTES from kaggle: https://www.kaggle.com/datasets/andrewmvd/board-games
######
fields = []
rows = []

with open('bgg_dataset.csv','r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=';')

    fields = next(csvreader)

    for row in csvreader:
        rows.append(row)

    print(f"Total no. of rows: {csvreader.line_num}")

for field in fields:
    print(field)

print(f'\nFirst 5 rows are:\n')
for row in rows[:5]:
    for col in row:
        print(col,end=" ")
    print('\n')


#READ IN API REVIEW DATA FROM BOARDGAME GEEK XML API: https://boardgamegeek.com/wiki/page/BGG_XML_API#
######
#using the requests module to grab the xml data from the bgg api and then the xmltodict module to manipulate
#the xml as a json object
r = requests.get('https://boardgamegeek.com/xmlapi/boardgame/174430')
obj = xmltodict.parse(r.text)
# print(json.dumps(obj))
game = json.loads(json.dumps(obj))['boardgames']['boardgame'] #converting nested ordereddict to a dict: https://www.geeksforgeeks.org/how-to-convert-a-nested-ordereddict-to-dict/
print(type(game))
# print(game)
print(game.keys())