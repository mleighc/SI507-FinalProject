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


##################################
###Function for Games Questions###
##################################
def ask(tree):
    """
    if the tree is a leaf, ask whether the object is the object named in the leaf
    if not - ask the question in the tree. If user says 'yes', call the function recursively on the subtree that is the second element in the triple
        or else if the user answers 'no', recur on the subtree that is the third element in the triple

    parameters:
        tree: 3-tuple or triple

    returns:
        tree: returns a new subTree whether or not the computer guesses the correct answer
        """
    if isLeaf(tree):
        new_tree = playLeaf(tree)
        return new_tree
    else:
        prompt = input(f'{tree[0]} ')
        if yes(prompt):
            n = ask(tree[1])
            return tuple([tree[0], n, tree[2]])
        else:
            n = ask(tree[2])
            return tuple([tree[0], tree[1], n])

def isLeaf(tree):
    '''
    match the pattern for a leaf node vs. a question/internal node based on the tuple pattern
    parameters:
        tree: node, triple, or tuple of tuples
    returns:
        boolean: true if the item is a leaf node and false if the item is an internal node
    '''
    # match tree:
    #     case (_, None, None):
    #         return True
    #     case _:
    #         return False
    text,left,right=tree
    if left is None and right is None:
        return True
    return False

def yes(prompt):
    '''
    checks if the user's input is yes or no
    paramters:
        a string received from a user input request
    returns:
        True if the user enters yes from a list of options or False if the user inputs anything else
        '''
    if prompt.lower().strip() in ('yes', 'y', "yup", "sure", 'yeah', 'yea'):
        return True
    return False

def playLeaf(tree):
    '''
    prompts the user with a question and prints a response based on their input
    parameters:
        tree: a triple or Leaf with a guess and 2 None values
    returns:
        printed response based on user input
    '''
    text,left,right = tree
    prompt = input(f'Is it {text}? ')
    if yes(prompt):
        print('I got it!')
        return tree
        # return True
    else:
        thing = input('Drats! What was it? ')
        new_q = input(f'What\'s a question that distinguishes between {thing} and {text}? ')
        # answer = input('And what\'s the answer for a car? ')
        newTree = (new_q.strip(), (thing.strip(), None, None), tree)
        return newTree
        # return False


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
    # print(f'Count of dictionaries with Multiplayer Strategy Games:{len(strat_multi)}')
    # print(f'Count of dictionaries with Multiplayer Customizable Games:{len(custom_multi)}')

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

    ######Parsing Diff/Easy Multiplayer Customizable Games
    custom_diff_multi = []
    custom_easy_multi = []
    for item in custom_multi:
        if item['Complexity Average'] > 2.5:
            custom_diff_multi.append(item)
        if item['Complexity Average'] < 2.5:
            custom_easy_multi.append(item)
    # print(f'Count of dictionaries with Multiplayer Difficult Customizable Games:{len(custom_diff_multi)}')
    # print(f'Count of dictionaries with Multiplayer Easy Customizable Games:{len(custom_easy_multi)}')

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

    print(f'\nBy answering the following questions, I will be able to help you decide what game to play next!')

    # '',[],[]

    ['Are you looking for a game to play solo or with others?',
        ['Solo',
            ['Do you have time for a short or a long game?',
                ['Short',
                    ['Do you prefer thematic or strategy games?',
                        ['Thematic',
                            ["SOLO SHORT THEMATIC GAMES LIST"],
                            []
                        ],
                        ['Strategy',
                            ["SOLO SHORT STRATEGY GAMES LIST"],
                            []
                        ]
                    ],
                    []
                ],
                ['Long',
                    ['Do you prefer thematic or strategy games?',
                        ['Thematic',["SOLO LONG THEMATIC GAMES LIST"],[]],
                        ['Strategy',["SOLO LONG STRATEGY GAMES LIST"],[]]
                    ],
                    []
                ]
            ],
            []
        ],
        ['With Others',
            ['Are you with Friends or Family?',
                ['Friends',
                    ['Do you prefer Strategy or Party Games?',
                        ['Strategy',[],[]],
                        ['Party',[],[]]],
                    []],
                ['Family',
                    ['Are there children in your group?',
                        ['Yes',[],[]],
                        ['No',[],[]]],
                    []
                ]
            ],
            []
        ]
    ] #1 tree example

    tree = [
        'a: Are you looking for a game to play solo or with others?',
    ['b: Do you have time for a short or a long game?',
    ['d: Do you prefer thematic or strategy games?',['h: Select a game from the list below to view the description and cover image: ',[short_solo_theme],[]],['i:Select a game from the list below to view the description and cover image: ',[short_solo_strat],[]]],
    ['e: Enter the Game ID to view the description and cover image: ',[long_solo],[]]],
    ['c: Are you with Friends or Family? ',
    ['f: Do you prefer Strategic or Customizable Games? ',['k: Do you want a challenge? ',['Enter the Game ID to view the descrition and cover image: ',[strat_diff_multi],[]],['Enter the Game ID to view the descrition and cover image: ',[strat_easy_multi],[]]],
    ['l: Do you want a challenge? ',['q: Enter the Game ID to view the descrition and cover image: ',[custom_diff_multi],[]],['r: Enter the Game ID to view the descrition and cover image: ',[custom_easy_multi],[]]]],
    ['g: Are there children in your group? ',['m: Do you want a challenge? ',['s: Enter the Game ID to view the descrition and cover image: ',[fam_diff_multi],[]],['t: Enter the Game ID to view the descrition and cover image: ',[fam_easy_multi],[]]],
    ['n: Enter the Game ID to view the descrition and cover image: ',[child_easy_multi],[]]]]
    ]


    test = ask(tree)
    print(test)






if __name__ == "__main__":
    main()