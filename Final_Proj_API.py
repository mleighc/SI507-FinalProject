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

######
#Write a csv file
def write_csv(filename, header, data):
    '''DOCSTRING!'''
    with open(filename, 'w', encoding='UTF8') as fileobj:
        writer = csv.writer(fileobj)

        writer.writerow(header)
        writer.writerow(data)

######
#write a dictionary to json
#helper functions below (write_json and write_dicts_to_csv) borrowed from SI506 Problem Sets written by Anthony Whyte
def write_json(filepath, data, encoding='utf-8', ensure_ascii=False, indent=2):
    """Serializes object as JSON. Writes content to the provided filepath.

    Parameters:
        filepath (str): the path to the file
        data (dict)/(list): the data to be encoded as JSON and written to the file
        encoding (str): name of encoding used to encode the file
        ensure_ascii (str): if False non-ASCII characters are printed as is; otherwise
                            non-ASCII characters are escaped.
        indent (int): number of "pretty printed" indention spaces applied to encoded JSON

    Returns:
        None
    """

    with open(filepath, 'w', encoding=encoding) as file_obj:
        json.dump(data, file_obj, ensure_ascii=ensure_ascii, indent=indent)


def main():
    '''DOCSTRING!'''
    # data = read_csv('bgg_dataset.csv')
    # print(data)
    
    # # filename = 'game_csv_test.csv'
    # # header = fields
    # # data = rows
    # # write_csv(filename,header,rows)
    


##############################################################
#READ IN API DATA FROM BOARDGAME GEEK XML API (SET UP SEARCH)#: https://boardgamegeek.com/wiki/page/BGG_XML_API#
##############################################################
# #using the requests module to grab the xml data from the bgg api and then the xmltodict module to manipulate
# #the xml as a json object

######
#FIRST: Retrieving boardgame items listed as HOT on bgg in order to recommend them as most popular
######
r = requests.get('https://boardgamegeek.com/xmlapi2/hot?boardgame')
obj = xmltodict.parse(r.text)
hot_items = json.loads(json.dumps(obj))['items']['item'] #converting nested ordereddict to a dict: https://www.geeksforgeeks.org/how-to-convert-a-nested-ordereddict-to-dict/

# for item in hot_items[:1]:
#     print(item)

hot_item_data = [] 
d = {}
for item in hot_items:
    for k,v in item.items():
        if k in ('@id', '@rank'): #fixing the keys with extra symbols
            k = k.split('@')[1] #access the key without the extra symbol
            d[k] = v
        if k in ('thumbnail', 'name', 'yearpublished'): #removing the nested dictionaries to have simply k,v pairs
            d[k] = v['@value']
    d['hot'] = 1
    d['type'] = 'boardgame'
    hot_item_data.append(d.copy()) #creating a list of dictionaries
    d.clear() #emptying the dict to start on the next dictionary to be appended
print(len(hot_item_data))
print(hot_item_data)
######
# #write this to json file
######
filepath = 'hot_boardgames.json'
write_json(filepath,hot_item_data)


if __name__ == '__main__':
    main()