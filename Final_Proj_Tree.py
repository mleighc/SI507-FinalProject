from cmath import inf
import json

class TreeNode:
    def __init__(self, val=None):
        if val != None:
            self.val = val
        else:
            self.val = None
        self.left = None
        self.right = None

    def printTree(self):
        print(self.val)

    def insert(self, val):
        if self.val:
            if val < self.val:
                    if self.left is None:
                        self.left = TreeNode(val)
                    else:
                        self.left.insert(val)
            elif val > self.val:
                    if self.right is None:
                        self.right = TreeNode(val)
                    else:
                        self.right.insert(val)
        else:
            self.val = val

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
    #read in the bgg_list json file prepped in Final_Proj_API.py
    filepath = 'bgg_list.json'
    bgg_list = read_json(filepath)
    print(bgg_list[0])

    #what's the range of Max/Min Player counts?
    max_of_max_players = 0
    min_of_min_players = float(inf)
    for item in bgg_list:
        if item['Max Players'] >= max_of_max_players:
            max_of_max_players = item['Max Players']
        if item['Min Players'] <= min_of_min_players:
            min_of_min_players = item['Min Players']
    print(f'Highest Max Players Count: {max_of_max_players}')
    print(f'Lowest Min Players Count: {min_of_min_players}')













if __name__ == "__main__":
    main()