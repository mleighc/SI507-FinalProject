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

    ##########################
    #####READ IN THE DATA#####
    ##########################
    #read in the bgg_list json file prepped in Final_Proj_API.py
    filepath = 'bgg_list.json'
    bgg_list = read_json(filepath)
    # print(bgg_list[0])
    
    ##########################
    #####MAX PLAYER COUNTS####
    ##########################
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
            solitary_games_names.append((item['Name'], item['Play Time'], item['Domains'], item['Complexity Average']))
            solitary_games.append(item)
    # print(f'List of Solitary Games for 1 Player Names: {solitary_games_names}')
    # print(f'Count of dictionaries with Solitary Games Attributes:{len(solitary_games)}')

    #####LONG SOLO GAMES
    long_solo = []
    #long = over an hour?
    #short = under an hour?
    for item in solitary_games:
        if item['Play Time'] > 60:
            long_solo.append(item)
    # print(f'Long Solo Games: {long_solo}')
    # print(f'Long Solo Games Count: {len(long_solo)}')

    #####SHORT SOLO THEMATIC/STRATEGIC GAMES
    short_solo = []
    #long = over an hour?
    #short = under an hour?
    for item in solitary_games:
        if item['Play Time'] < 60:
            short_solo.append(item)
    
    short_solo_theme = []
    short_solo_strat = []
    for item in short_solo:
        for t in item['Domains']:
            if t == 'Thematic Games':
                short_solo_theme.append(item)
            if t == 'Strategy Games':
                short_solo_strat.append(item)
    # print(f'Short Solo Thematic Games Count: {len(short_solo_theme)}')
    # print(f'Short Solo Strategic Games Count: {len(short_solo_strat)}')


    ######################
    ##Parsing MULTI GAMES##
    ######################

    ###### MULTIPLAYER GAMES
    #grabbing all multiplayer games and checking their unique types
    multiplayer = []
    multiplayer_names = []
    for item in bgg_list:
        if item['Max Players'] > 1:
            multiplayer_names.append((item['Name'], item['Play Time'], item['Domains'], item['Complexity Average']))
            multiplayer.append(item)
    # print(f'List of Multiplayer Games for Friends Names: {multiplayer_names}')
    # print(f'Count of dictionaries with Multiplayer Games Attributes:{len(multiplayer)}')

    #####Parsing Strategic and Customizable Multiplayer Games
    strat_multi = []
    custom_multi = []
    for item in multiplayer:
        for t in item['Domains']:
            if t == 'Strategy Games':
                strat_multi.append(item)
            elif t == 'Customizable Games':
                custom_multi.append(item)
    print(f'Count of dictionaries with Multiplayer Strategy Games:{len(strat_multi)}')
    print(f'Count of dictionaries with Multiplayer Customizable Games:{len(custom_multi)}')

    ######Parsing Diff/Easy Multiplayer Strategy Games
    strat_diff_multi = []
    strat_easy_multi = []
    for item in strat_multi:
        if item['Complexity Average'] > 2.5:
            strat_diff_multi.append(item)
        if item['Complexity Average'] < 2.5:
            strat_easy_multi.append(item)
    print(f'Count of dictionaries with Multiplayer Difficult Strategy Games:{len(strat_diff_multi)}')
    print(f'Count of dictionaries with Multiplayer Easy Strategy Games:{len(strat_easy_multi)}')

    ######Parsing Diff/Easy Multiplayer Customizable Games
    custom_diff_multi = []
    custom_easy_multi = []
    for item in custom_multi:
        if item['Complexity Average'] > 2.5:
            custom_diff_multi.append(item)
        if item['Complexity Average'] < 2.5:
            custom_easy_multi.append(item)
    print(f'Count of dictionaries with Multiplayer Difficult Customizable Games:{len(custom_diff_multi)}')
    print(f'Count of dictionaries with Multiplayer Easy Customizable Games:{len(custom_easy_multi)}')

    # multiplayer_types = set()
    # for item in multiplayer:
    #     for t in item['Domains']:
    #         multiplayer_types.add(t)
    # print(f'Types of Multiplayer Games: {multiplayer_types}')

    ####################
    ##Loading the Tree##
    ####################
    '''Notes for me:
    I want to set up the tree by nesting each of the subtrees with a question and then the resulting question or game suggestion,
    then I want to prep and store the filtered data into variables and add them into their respective locations in the tree structures.
    Finally, I will write some functions/code to traverse the tree, ask the user questions and then pop out more questions or
    suggested games based on their responses'''

    # print(f'\nBy answering the following questions, I will be able to help you decide what game to play next!')

    ['',[],[]] #1 tree

    tree = [
        'a: Are you looking for a game to play solo or with others?',
    ['b: Do you have time for a short or a long game?',
    ['d: Do you prefer thematic or strategy games?',['h: Select a game from the list below to view the description and cover image: ',[short_solo_theme],[]],['i:Select a game from the list below to view the description and cover image: ',[short_solo_strat],[]]],
    ['e: Enter the Game ID to view the description and cover image: ',[long_solo],[]]],
    ['c: Are you with Friends or Family? ',
    ['f: Do you prefer Strategic or Customizable Games? ',['k: Do you want a challenge? ',['Enter the Game ID to view the descrition and cover image: ',[strat_diff_multi],[]],['Enter the Game ID to view the descrition and cover image: ',[strat_easy_multi],[]]],
    ['l: Do you want a challenge? ',['q: Enter the Game ID to view the descrition and cover image: ',[custom_diff_multi],[]],['r: Enter the Game ID to view the descrition and cover image: ',[custom_easy_multi],[]]]],
    ['g: Are there children in your group? ',['m: Do you want a challenge? ',['s: Enter the Game ID to view the descrition and cover image: ',['FAMILY DIFFICULT LIST'],[]],['t: Enter the Game ID to view the descrition and cover image: ',['FAMILY EASY LIST'],[]]],
    ['n: Do you want a challenge? ',['u: Enter the Game ID to view the descrition and cover image: ',['CHILDREN\'S GAMES DIFFICULT LIST'],[]],['v: Enter the Game ID to view the descrition and cover image: ',['CHILDREN\'S GAMES EASY LIST'],[]]]]]
    ]




if __name__ == "__main__":
    main()