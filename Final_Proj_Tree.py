# import Final_Proj_API as fpa

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

def main():
    '''
    DOCSTRING!
    '''
    root = TreeNode(10)
    root.printTree()












if __name__ == "__main__":
    main()