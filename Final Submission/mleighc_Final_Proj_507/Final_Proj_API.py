import requests
import csv
import xmltodict, json

####################################
#READ IN A CSV WITH GAME ATTRIBUTES# from kaggle: https://www.kaggle.com/datasets/andrewmvd/board-games
####################################

#a couple of helper functions below (write_json and write_dicts_to_csv) borrowed from SI506 Problem Sets written by Anthony Whyte
def read_csv_to_dicts(filepath, encoding='utf-8-sig', newline='', delimiter=';'):
    """Accepts a file path, creates a file object, and returns a list of
    dictionaries that represent the row values using the cvs.DictReader().

    Parameters:
        filepath (str): path to file
        encoding (str): name of encoding used to decode the file
        newline (str): specifies replacement value for newline '\n'
                       or '\r\n' (Windows) character sequences
        delimiter (str): delimiter that separates the row values

    Returns:
        list: nested dictionaries representing the file contents
     """

    with open(filepath, 'r', newline=newline, encoding=encoding) as file_obj:
        data = []
        reader = csv.DictReader(file_obj, delimiter=delimiter)
        for line in reader:
            data.append(line) # OrderedDict()
            # data.append(dict(line)) # convert OrderedDict() to dict

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

##including this function within the one below instead
# def clean_string(value):
#     '''
#     Accepts a string value and replaces HTML entities with spaces or quotations
#     parameters:
#         value: a string to be cleaned
#     returns:
#         value: the same string with the HTML entities removed
#         '''
#     value= value.replace('<br/><br/>', ' ')
#     value=value.replace('&ldquo;', '\'')
#     value=value.replace('&rdquo;', '\'')
#     return value

def clean_json(json_obj):
    ''' 
    Accepts a json object and iterates through the keys to clean up the necessary values i.e. comma separated numbers to floats, removing html entities from strings, and stripping string values
    parameters:
        json_obj: a json object
    returns:
        json_obj: the same json object with cleaned values
    '''
    for k in json_obj.keys():
        if k in ('Rating Average', 'Complexity Average'):
            json_obj[k]=json_obj[k].replace(',', '.')
            json_obj[k]=float(json_obj[k])
        if k in ('ID','Year Published', 'Min Players','Max Players','Play Time','Min Age'):
            json_obj[k]=int(json_obj[k])
        if k == "Description":
            json_obj[k]=json_obj[k].replace('<br/><br/>', ' ')
            json_obj[k]=json_obj[k].replace('&ldquo;', '\'')
            json_obj[k]=json_obj[k].replace('&rdquo;', '\'')
            json_obj[k]=json_obj[k].replace('&rsquo;', '\'')
        if k == "Domains":
            for i in range(len(json_obj[k])):
                json_obj[k][i]=json_obj[k][i].strip()
    return json_obj

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
hot_items = json.loads(json.dumps(obj))['items']['item'] 
#converting nested ordereddict to a dict: https://www.geeksforgeeks.org/how-to-convert-a-nested-ordereddict-to-dict/

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
# print(len(hot_item_data))
# print(hot_item_data)


#####
#Grabbing names of hot items to be able to indicate their hot item field as 1 in the later dataset
#####
hot_name_list = []
for name in hot_item_data:
    hot_name_list.append(name['name'])
# print(hot_name_list)


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
    item['Description'] = descr
    item['Image'] = image
    item['Category_list'] = categ

######
# #write hot_item_data to json file
######
filepath = 'hot_boardgames.json'
write_json(filepath,hot_item_data)

MY_FIELDS = [
    'ID',
    'Name',
    'Year Published',
    'Min Players',
    'Max Players',
    'Play Time',
    'Min Age',
    'Rating Average',
    'Complexity Average',
    'Domains'
]

######
# NEXT: read in the bgg_dataset.csv, remove the unnecessary field and add some from the API that are more interesting (i.e. I want to try to display the image files for users when they pick a game)
######
#Read in bgg_dataset.csv to continue to enhance board game data
filepath = 'bgg_dataset.csv'
bgg = read_csv_to_dicts(filepath)
# print(bgg[0])

######
# Grabbing only the fields I want
######
bgg_list = []
d = {}
for item in bgg:
    for key,val in item.items():
        if key in MY_FIELDS:
            d[key] = val
        if key == 'Domains':
            d[key] = val.split(',')
    bgg_list.append(d.copy())
    d.clear()
# print(met_dog_data)
# print(len(bgg_list))
print(bgg_list[0])

#just pulling a subset to be loaded into the tree - since 20k+ is too many for my computer to handle during testing
bgg_subset = bgg_list[:1000:2]

#looping over the subset to enhance their information with descriptions, images, category lists, and asses whether they are hot items.
for item in bgg_subset:
    id = item['ID']
    r = requests.get(f'https://boardgamegeek.com/xmlapi/boardgame/{id}')
    obj = xmltodict.parse(r.text)
    obj_details = json.loads(json.dumps(obj))['boardgames']['boardgame']
    # print(obj_details)

    #description needs to be cleaned since it has line breaks indicated as <br>
    descr = obj_details['description']
    #image URL
    image = obj_details['image']
    #categories are nested in a list of dictionaries
    categ = []
    try:
        if isinstance(obj_details['boardgamecategory'],list):
            for i in obj_details['boardgamecategory']:
                categ.append(i['#text'])
        else:
            categ.append(obj_details['boardgamecategory']['#text'])
    except KeyError:
        categ = [None]

    item['Description'] = descr
    item['Image'] = image
    item['Category_list'] = categ
    #check if boardgame in list of "hot items", default is 0 (False)
    item['Hot Item?'] = 0
    if item["Name"] in hot_name_list:
        item['Hot Item?'] += 1

    #clean the json object
    clean_json(item)

print(len(bgg_subset))


######
#write bgg_list to json file to be read into file for implmening tree
######
filepath = 'bgg_list.json'
write_json(filepath,bgg_subset)


if __name__ == '__main__':
    main()