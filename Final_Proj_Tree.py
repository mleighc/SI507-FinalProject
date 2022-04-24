from cmath import inf
import json

# class TreeNode:
#     def __init__(self, val=None):
#         if val != None:
#             self.val = val
#         else:
#             self.val = None
#         self.left = None
#         self.right = None

#     def printTree(self):
#         print(self.val)

#     def insert(self, val):
#         if self.val:
#             if val < self.val:
#                     if self.left is None:
#                         self.left = TreeNode(val)
#                     else:
#                         self.left.insert(val)
#             elif val > self.val:
#                     if self.right is None:
#                         self.right = TreeNode(val)
#                     else:
#                         self.right.insert(val)
#         else:
#             self.val = val

#helper function referenced from SI506 lectures
def read_json(filepath, encoding='utf-8'):
    """Reads a JSON document, decodes the file content, and returns a list or
    dictionary if provided with a valid filepath.

    Parameters:
        filepath (str): path to file
        encoding (str): name of encoding used to decode the file

    Returns:
        dict/list: dict or list representations of the decoded JSON document
    """

    with open(filepath, 'r', encoding=encoding) as file_obj:
        return json.load(file_obj)

def main():
    '''
    DOCSTRING!
    '''
    ###############################################
    ##Analyzing the Data and Prepping it for Tree##
    ###############################################

    #####READ IN THE DATA
    #read in the bgg_list json file prepped in Final_Proj_API.py
    filepath = 'bgg_list.json'
    bgg_list = read_json(filepath)
    # print(bgg_list[0])

    #####MAX PLAYER COUNTS
    #what's the range of Max/Min Player counts?
    max_of_max_players = 0
    min_of_min_players = float(inf)
    for item in bgg_list:
        if item['Max Players'] >= max_of_max_players:
            max_of_max_players = item['Max Players']
        if item['Min Players'] <= min_of_min_players:
            min_of_min_players = item['Min Players']
    # print(f'Highest Max Players Count: {max_of_max_players}')
    # print(f'Lowest Min Players Count: {min_of_min_players}')

    #####UNDERSTANDING DOMAINS
    #what are the different domains i.e. types of games? 
    domain_list = []
    for i in bgg_list:
        for t in i['Domains']:
            if t not in domain_list:
                domain_list.append(t)
    # print(f'List of all represented Domains: {domain_list}')

    #####FAMILY GAMES
    family_list = []
    family_list_names =[]
    for i in bgg_list:
        for t in i['Domains']:
            if t == 'Family Games':
                family_list.append(i)
                family_list_names.append(i['Name'])
    # print(f'List of Family Games: {family_list_names}')
    # print(f'Count of dictionaries with Family Game Domain:{len(family_list)}')

    ######################
    ##Parsing SOLO GAMES##
    ######################

    #####ALL SOLO GAMES
    #how many games are solitary games and what are their types i.e. have max player count of 1?
    solitary_games = []
    solitary_games_names = []
    for item in bgg_list:
        if item['Max Players'] == 1:
            solitary_games_names.append((item['Name'], item['Play Time'], item['Domains']))
            solitary_games.append(item)
    print(f'List of Solitary Games for 1 Player Names: {solitary_games_names}')
    print(f'Count of dictionaries with Solitary Games Attributes:{len(solitary_games)}')

    #####LONG SOLO GAMES
    long_solo = []
    #long = over an hour?
    #short = under an hour?
    for item in solitary_games:
        if item['Play Time'] > 60:
            long_solo.append(item)
    print(f'Long Solo Games: {long_solo}')

    # solitary_types = set()
    # for item in solitary_games:
    #     for t in item['Domains']:
    #         solitary_types.add(t)
    # print(f'Types of Solitary Games: {solitary_types}')

    ######################
    ##Parsing MULTI GAMES##
    ######################

    ###### MULTIPLAYER GAMES
    #grabbing all multiplayer games and checking their unique types
    multiplayer = []
    multiplayer_names = []
    for item in bgg_list:
        if item['Max Players'] > 1:
            multiplayer_names.append(item['Name'])
            multiplayer.append(item)
    # print(f'List of Multiplayer Games for Friends Names: {multiplayer_names}')
    # print(f'Count of dictionaries with Multiplayer Games Attributes:{len(multiplayer)}')

    multiplayer_types = set()
    for item in multiplayer:
        for t in item['Domains']:
            multiplayer_types.add(t)
    # print(f'Types of Multiplayer Games: {multiplayer_types}')

    ####################
    ##Loading the Tree##
    ####################
    tree = [
        'Are you looking for a game to play solo or with others?', #root A
        [
            'Do you prefer Strategy or Thematic Games?', #subTree1 Solo/1Player B
            [
                'Placeholder:Strategy',#leftTree Strategy Games D
                [
                    'Difficult or Easy?',
                    ['Placeholder:List of Easy'],
                    ['Placeholder: List of Difficult']
                ],[], 
            [
                'Placeholder:Thematic',# rightTree Thematic Games E
                [
                    'Difficult or Easy?',
                    ['Placeholder:List of Easy'],
                    ['Placeholder: List of Difficult']
        ],
        [
            'Are you with Friends or Family?', #subTree1 With Others/Multiplayer C
            ['Placeholder:Friends',[],[]], #F
            ['Placeholder:Family',[],[]] #G
        ]
        ]]]]

    '''Notes for me:
    I want to set up the tree by nesting each of the subtrees with a question and then the resulting question or game suggestion,
    then I want to prep and store the filtered data into variables and add them into their respective locations in the tree structures.
    Finally, I will write some functions/code to traverse the tree, ask the user questions and then pop out more questions or
    suggested games based on their responses'''

    # print(f'\nBy answering the following questions, I will be able to help you decide what game to play next!')

    ['',[],[]] #1 tree

    tree = ['a',
    ['b',
    ['d',['h',[],[]],['i',[],[]]],
    ['e',['j',[],[]],[]]],
    
    ['c',
    ['f',
    ['k',['o',[],[]],['p',[],[]]],
    ['l',['q',[],[]],['r',[],[]]]],
    ['g',['m',['s',[],[]],['t',[],[]]],
    ['n',['u',[],[]],['v',[],[]]]]]]










    ]




if __name__ == "__main__":
    main()