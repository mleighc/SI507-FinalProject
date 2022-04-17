from dataclasses import dataclass
import requests
import csv
import xmltodict, json

####################################
#READ IN A CSV WITH GAME ATTRIBUTES# from kaggle: https://www.kaggle.com/datasets/andrewmvd/board-games
####################################

def read_csv(filename):
    ''''DOCSTRING!'''
    with open(filename,'r') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=';')
        line_count = 0
        data = []
        # print(type(csv_reader))

        for row in csv_reader:
            data.append(row)
            return data
            # if line_count == 0:
        #         print(f'Column names are {", ".join(row)}')
        #         line_count += 1
        #     else:
        #         print(", ".join(row))
        #         line_count += 1
    # print(f'Processed {line_count} lines.')


def write_csv(filename, header, data):
    '''DOCSTRING!'''
    with open(filename, 'w', encoding='UTF8') as fileobj:
        writer = csv.writer(fileobj)

        writer.writerow(header)
        writer.writerow(data)





##############################################################
#READ IN API DATA FROM BOARDGAME GEEK XML API (SET UP SEARCH)#: https://boardgamegeek.com/wiki/page/BGG_XML_API#
##############################################################
# #using the requests module to grab the xml data from the bgg api and then the xmltodict module to manipulate
# #the xml as a json object

#FIRST: Retrieving items listed as HOT on bgg in order to recommend them as most popular
r = requests.get('https://boardgamegeek.com/xmlapi2/hot?boardgame')
obj = xmltodict.parse(r.text)
# print(json.dumps(obj))
hot_items = json.loads(json.dumps(obj))['items']['item'] #converting nested ordereddict to a dict: https://www.geeksforgeeks.org/how-to-convert-a-nested-ordereddict-to-dict/
for item in hot_items:
    print(item)
    print('\n')



def main():
    '''DOCSTRING!'''
    # data = read_csv('bgg_dataset.csv')
    # print(data)
    
    # # filename = 'game_csv_test.csv'
    # # header = fields
    # # data = rows
    # # write_csv(filename,header,rows)
    pass


if __name__ == '__main__':
    main()