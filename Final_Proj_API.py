from unicodedata import category
import requests
import csv
import xmltodict, json

####################################
#READ IN A CSV WITH GAME ATTRIBUTES# from kaggle: https://www.kaggle.com/datasets/andrewmvd/board-games
####################################

#a couple of helper functions below (write_json and write_dicts_to_csv) borrowed from SI506 Problem Sets written by Anthony Whyte
def read_csv(filepath, encoding='utf-8', newline='', delimiter=','):
    """
    Reads a CSV file, parsing row values per the provided delimiter. Returns a list
    of lists, wherein each nested list represents a single row from the input file.

    Parameters:
        filepath (str): The location of the file to read.
        encoding (str): name of encoding used to decode the file.
        newline (str): specifies replacement value for newline '\n'
                       or '\r\n' (Windows) character sequences.
        delimiter (str): delimiter that separates the row values

    Returns:
        list: a list of nested "row" lists
    """

    with open(filepath, 'r', encoding=encoding, newline=newline) as file_obj:
        data = []
        reader = csv.reader(file_obj, delimiter=delimiter)
        for row in reader:
            data.append(row)

        return data

######
#write a dictionary to json
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
# print(hot_item_data)

######
# NEXT: Enhance the data in this dictionary with additional features from BGG API, access individual HOT boardgames by their ID
######
#iterate over hot items list to grab the id and run an API request for each individual game within that list
for item in hot_item_data:
    id = item['id']
    r = requests.get(f'https://boardgamegeek.com/xmlapi/boardgame/{id}')
    obj = xmltodict.parse(r.text)
    obj_details = json.loads(json.dumps(obj))['boardgames']['boardgame']


    ####grab features to add to my dicts in hot_item_data
    #description needs to be cleaned since it has line breaks indicated as <br>
    descr = obj_details['description']
    #image URL
    image = obj_details['image']
    #categories are nested in a list of dictionaries
    categ = []
    if isinstance(obj_details['boardgamecategory'],list):
        for i in obj_details['boardgamecategory']:
            categ.append(i['#text'])
    else:
        categ.append(obj_details['boardgamecategory']['#text'])


    ###update the item's dictionary with these added features
    item['description'] = descr
    item['image'] = image
    item['category_list'] = categ

######
#Read in bgg_dataset.csv to continue to enhance board game data
filepath = 'bgg_dataset.csv'
bgg = read_csv(filepath)
print(len(bgg))

######
# #write hot_item_data to json file
######
# filepath = 'hot_boardgames.json'
# write_json(filepath,hot_item_data)


if __name__ == '__main__':
    main()