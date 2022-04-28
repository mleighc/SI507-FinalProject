from cmath import inf
import json
import webbrowser

#####################################################
#################HELPER FUNCTIONS####################
#####################################################

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

def clean_string(s):
    '''
    iterate over a series of html entities to clean them from a string
    parameters:
        s: string
    returns:
        s: cleaned string
    '''
    for r in (('&quot;','\"'),
    ('&ldquo;','\"',),
    ('&rdquo;','\"'),
    ('&rsquo;','\"'), 
    ('</a>',' '),
    ('<br/>',' '), 
    ('<br>',' '), 
    ('P&amp;P', ' '),
    ('&bull;', ' ')):
        s = s.replace(*r)
    return s


#################################################################
#################GAME QUESTION FLOW FUNCTIONS####################
#################################################################

def display_list(games):
        '''
        iterates over the 1st index element of a subTree (which is a list) and prints the formatted Game ID and Name of each item
        parameters:
            games: subTree or list of 3 lists
        returns:
            None
        '''
        print(f'\n')
        for item in games[1]:
            print(f'{item["ID"]}: {item["Name"]}')

def viewDesc(item):
    '''
        accesses the Description key of a passed in Game object (1 dictionary represents 1 game), calls the clean_string function to remove html entities, and prints the description to the command line
        parameters:
            item: a dictionary
        returns:
            None
    '''
    desc = item['Description']
    d = clean_string(desc)
    print(f'\n{d}')

def viewImage(item):
    '''
        accesses the url or "Image" key of a dictionary and opens the url in a webbrowser
        parameters:
            item: a dictionary
        returns:
            None
    '''
    url = item['Image']
    webbrowser.open(url,new=1)

def pickGame(tree):
    '''
        prompts the user to select the Game ID for the game they'd like to view or exit the program if they have finished
        will reprompt the user to pick a new ID after each selection
        calls the viewDesc and viewImage functions to display key information to the user
        parameters:
            tree: a subTree or triple of lists
        returns:
            None
    '''
    while True:
        prompt = input(f'\nWould you like to view more information? Enter the Game ID to view the game description and cover image or "Exit" to exit the program. ')
        if prompt in ('exit','EXIT','Exit'):
            break
        else:
            for item in tree[1]:
                if item['ID'] == int(prompt):
                    viewDesc(item)
                    viewImage(item)

def isListResult(tree):
    '''
    unpacks the subtree to check if it is the final result leaf
    parameters:
        tree: a subTree or triple of lists
    returns:
        returns: boolean; True if it is a leaf or ListReult and False otherwise
    '''
    text,left,right = tree
    if isinstance(text[1], list) and left is None and right is None:
        return True
    return False

def ask(tree):
    '''
    checks if the subtree is leaf or ListResult of the tree
    if it is:
        the final list of suggested games is displayed to the user (i.e. the display_list function called), then calls the pickGame to prompt the user to view more game information
    if it is not:
        unpacks the tree, prompts the user with the first question in the tree, then calls itself recursively based on the user's selection i.e. whether the user picked the respons in the left or right subTree
    parameters:
        tree: a subTree or triple of lists
    returns:
        None
    '''
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

#################################################################
#########################MAIN FUNCTION###########################
#################################################################

def main():
    """Entry point for program.

    Parameters:
        None

    Returns:
        None
    """

    ############################################################
    #################READ and PARSE THE DATA####################
    ############################################################

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

    #####Parsing Strategic and Party Multiplayer Games
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

    ######parse short/long party games
    party_multi_short = []
    party_multi_long = []
    for item in party_multi:
        if item['Play Time'] < 60:
            party_multi_short.append(item)
        if item['Play Time'] > 60:
            party_multi_long.append(item)
    # print(f'Count of Short Party Games: {len(party_multi_short)}')
    # print(f'Count of Long Party Games: {len(party_multi_long)}')

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

    #######Parse Short/Long within Diff/Easy Strategy Games
    strat_diff_multi_short = []
    strat_diff_multi_long = []
    strat_easy_multi_short = []
    strat_easy_multi_long = [] 
    for item in strat_diff_multi:
        if item['Play Time'] < 60:
            strat_diff_multi_short.append(item)
        if item['Play Time'] > 60:
            strat_diff_multi_long.append(item)
    for item in strat_easy_multi:
        if item['Play Time'] < 60:
            strat_easy_multi_short.append(item)
        if item['Play Time'] > 60:
            strat_easy_multi_long.append(item)
    # print(f'Count of Short Diff Strategy Games: {len(strat_diff_multi_short)}')
    # print(f'Count of Long Diff Strategy Games: {len(strat_diff_multi_long)}')
    # print(f'Count of Short Easy Strategy Games: {len(strat_easy_multi_short)}')
    # print(f'Count of Long Easy Strategy Games: {len(strat_easy_multi_long)}')

    ######Parsing strat_diff_multi_long down to popular and regular games to reduce length of final list
    strat_diff_multi_long_popular = []
    strat_diff_multi_long_regular = []
    for item in strat_diff_multi_long:
        if item['Hot Item?'] == 1:
            strat_diff_multi_long_popular.append(item)
        if item['Hot Item?'] == 0:
            strat_diff_multi_long_regular.append(item)
    # print(f'Count of Long Diff Popular Strategy Games: {len(strat_diff_multi_long_popular)}')
    # print(f'Count of Long Diff Regular Strategy Games: {len(strat_diff_multi_long_regular)}')

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

    ####################################################################################
    #################LOAD TREE STRUCTURE WITH PARSED BOARD GAME DATA####################
    ####################################################################################

    tree = [['','Are you looking for a game to play solo or with others? '],
        [['Solo','Do you have time for a short or a long game? '],
            [['Short','Do you prefer thematic or strategy games? '],
                [['Thematic',short_solo_theme], None,None],
                [['Strategy',short_solo_strat], None,None]],
            [['Long',long_solo],None,None]],
        [['With Others','Are you with Friends or Family? '],
            [['Friends','Do you prefer Strategy or Party Games? '],
                [['Strategy','Do you want a challenge? '],
                    [['Yes','Do you have time for a short or a long game? '],
                        [['Short',strat_diff_multi_short],None,None],
                        [['Long','Do you want to see only the most popular games? '],
                            [['Yes',strat_diff_multi_long_popular],None,None],
                            [['No',strat_diff_multi_long_regular],None,None]]],
                    [['No','Do you have time for a short or a long game? '],
                        [['Short',strat_easy_multi_short],None,None],
                        [['Long',strat_easy_multi_long],None,None]]],
                [['Party','Do you have time for a short or a long game? '],
                    [['Short',party_multi_short],None,None],
                    [['Long',party_multi_long],None,None]]],
            [['Family','Are there children in your group? '],
                [['Yes',child_multi],None,None],
                [['No','Do you want a challenge? '],
                    [['Yes',fam_diff_multi],None,None],
                    [['No',fam_easy_multi],None,None]]]]]

    ##########################################################
    #################QUESTION CONTROL FLOW####################
    ##########################################################
    print(f'Answer my questions and I will help you decide on the next game to play!')
    while True:
        ask(tree)
        prompt = input('Would you like to start again? ')
        if prompt in ('Yes','yes','Y','y','YES'):
            continue
        else:
            quit()



if __name__ == "__main__":
    main()