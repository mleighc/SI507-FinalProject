from cmath import inf
import json
import webbrowser

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


##################################
###Functions for Games Questions###
##################################

def display_list(games):
        '''DOCSTRING!'''
        # count = 0
        for item in games[1]:
            print(f'\n{item["ID"]}: {item["Name"]}')

def viewDesc(item):
    '''DOCSTRING'''
    desc = item['Description']
    print(f'\n{desc}')

def viewImage(item):
    '''DOCSTRING'''
    url = item['Image']
    webbrowser.open(url,new=0)

def pickGame(tree):
    '''DOCSTRING!'''
    prompt = input(f'\nWould you like to view more information? Enter the Game ID to view the description and cover image or "Exit" to exit the program. ')
    if prompt in ('exit','EXIT','Exit'):
        quit()
    else:
        while True:
            if 
            for item in tree[1]:
                if item['ID'] == int(prompt):
                    viewDesc(item)
                    viewImage(item)

def isListResult(tree):
    '''DOCSTRING!'''
    text,left,right = tree
    if isinstance(text[1], list) and left is None and right is None:
        return True
    return False

def ask(tree):
    '''DOCSTRING!'''
    if isListResult(tree):
        display_list(tree[0])
        pickGame(tree[0])
    else:
        text,left,right = tree
        prompt = input(f'{text[1]} ')
        if prompt.lower().strip() == left[0][0].lower():
            ask(left)
        elif prompt.lower().strip() == right[0][0].lower():
            ask(right)

###################
###MAIN FUNCTION###
###################

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
    party_multi = []
    for item in multiplayer:
        for t in item['Domains']:
            if t == 'Strategy Games':
                strat_multi.append(item)
            elif t == 'Party Games':
                party_multi.append(item)
    # print(f'Count of dictionaries with Multiplayer Strategy Games:{len(strat_multi)}')
    # print(f'Count of dictionaries with Multiplayer Customizable Games:{len(party_multi)}')
    # print(type(party_multi))

    ######Parsing Diff/Easy Multiplayer Strategy Games
    strat_diff_multi = []
    strat_easy_multi = []
    for item in strat_multi:
        if item['Complexity Average'] > 2.5:
            strat_diff_multi.append(item)
        if item['Complexity Average'] < 2.5:
            strat_easy_multi.append(item)
    # print(f'Count of dictionaries with Multiplayer Difficult Strategy Games:{len(strat_diff_multi)}')
    # print(f'Count of dictionaries with Multiplayer Easy Strategy Games:{len(strat_easy_multi)}')

    # multiplayer_types = set()
    # for item in multiplayer:
    #     for t in item['Domains']:
    #         multiplayer_types.add(t)
    # print(f'Types of Multiplayer Games: {multiplayer_types}')

    #####Parsing Family and Children Multiplayer Games
    fam_multi = []
    child_multi = []
    for item in multiplayer:
        for t in item['Domains']:
            if t == "Children's Games":
                child_multi.append(item)
            elif t == 'Family Games':
                fam_multi.append(item)
    # print(f'Count of dictionaries with Multiplayer Family Games:{len(fam_multi)}')
    # print(f'Count of dictionaries with Multiplayer Children\'s Games:{len(child_multi)}')

    ######Parsing Diff/Easy Multiplayer Family Games
    fam_diff_multi = []
    fam_easy_multi = []
    for item in fam_multi:
        if item['Complexity Average'] > 2.5:
            fam_diff_multi.append(item)
        if item['Complexity Average'] < 2.5:
            fam_easy_multi.append(item)
    # print(f'Count of dictionaries with Multiplayer Difficult Family Games:{len(fam_diff_multi)}')
    # print(f'Count of dictionaries with Multiplayer Easy Family Games:{len(fam_easy_multi)}')

    ######Parsing Diff/Easy Multiplayer Customizable Games
    child_diff_multi = []
    child_easy_multi = []
    for item in child_multi:
        if item['Complexity Average'] > 2.5:
            child_diff_multi.append(item)
        if item['Complexity Average'] < 2.5:
            child_easy_multi.append(item)
    # print(f'Count of dictionaries with Multiplayer Difficult Children\'s Games:{len(child_diff_multi)}')
    # print(f'Count of dictionaries with Multiplayer Easy Children\'s Games:{len(child_easy_multi)}')

    ####################
    ##Loading the Tree##
    ####################
    '''Notes for me:
    I want to set up the tree by nesting each of the subtrees with a question and then the resulting question or game suggestion,
    then I want to prep and store the filtered data into variables and add them into their respective locations in the tree structures.
    Finally, I will write some functions/code to traverse the tree, ask the user questions and then pop out more questions or
    suggested games based on their responses'''

    # print(f'\nBy answering the following questions, I will be able to help you decide what game to play next!')

    # [],[],[]

    tree = [['','Are you looking for a game to play solo or with others?'],
        [['Solo','Do you have time for a short or a long game?'],
            [['Short','Do you prefer thematic or strategy games?'],
                [['Thematic','Enter the Game ID to view the game\'s description and cover image: '], [['',short_solo_theme],[],[]],[]],
                [['Strategy',short_solo_strat], None,None]],
            [['Long','Do you prefer thematic or strategy games? '],
                [['Thematic','Enter the Game ID to view the game\'s description and cover image: '],[[],[],[]],[]],
                [['Strategy','Enter the Game ID to view the game\'s description and cover image: '],[],[]]]],
        [['With Others','Are you with Friends or Family?'],[],[]]]

        #notes for me: need to finish the With Others section and display the lists of games before prompting user to pick a game id. Need to write a function 
        #to print the id and set some control flow in the test function to display the right data

    #tree = [['','Are you looking for a game to play solo or with others?'],
     #   ['Solo',
      #      ['Do you have time for a short or a long game?',
                #['Short',
                  #  ['Do you prefer thematic or strategy games?',
                        #['Thematic',['Enter the Game ID to view the game\'s description and cover image: ',[short_solo_theme],None],None],
                        # ['Strategy',['Enter the Game ID to view the game\'s description and cover image: ',[short_solo_strat],None],None]],None],
                #['Long',
                 #   ['Do you prefer thematic or strategy games? ',
    #                     ['Thematic',['Enter the Game ID to view the game\'s description and cover image: ',[long_solo_theme],None],None],
    #                     ['Strategy',['Enter the Game ID to view the game\'s description and cover image: ',[short_solo_strat],None],None]],None]],None],
    #  #   ['With Others',
    #   #      ['Are you with Friends or Family?',
    #             ['Friends',
    #                 ['Do you prefer Strategy or Party Games?',
    #                     ['Strategy',['Do you want a challenge?',
    #                         ['Yes',['Enter the Game ID to view the game\'s description and cover image: ',[strat_diff_multi],None],None],
    #                         ['No',['Enter the Game ID to view the game\'s description and cover image: ',[strat_easy_multi],None],None]],None],
    #                     ['Party',['Enter the Game ID to view the game\'s description and cover image: ',[party_multi],None],None]],None],
    #             ['Family',
    #                 ['Are there children in your group?',
    #                     ['Yes',['Enter the Game ID to view the game\'s description and cover image: ',[child_multi],None],None],
    #                     ['No',['Do you want a challenge?',['Yes',[fam_diff_multi],[]],['No',[fam_easy_multi],None]],None]],None]],None]]


    test = ask(tree)
    print(test)



if __name__ == "__main__":
    main()