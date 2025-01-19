import random
import matplotlib.pyplot as plt
import sys
class RBNode:

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.colour = "R"

    def get_uncle(self):
        return

    def is_leaf(self):
        return self.left == None and self.right == None

    def is_left_child(self):
        return self == self.parent.left

    def is_right_child(self):
        return not self.is_left_child()

    def is_red(self):
        return self.colour == "R"

    def is_black(self):
        return not self.is_red()

    def make_black(self):
        self.colour = "B"

    def make_red(self):
        self.colour = "R"

    def get_brother(self):
        if self.parent.right == self:
            return self.parent.left
        return self.parent.right

    def get_uncle(self):
        return self.parent.get_brother()

    def uncle_is_black(self):
        if self.get_uncle() == None:
            return True
        return self.get_uncle().is_black()

    def __str__(self):
        return "(" + str(self.value) + "," + self.colour + ")"

    def __repr__(self):
        return "(" + str(self.value) + "," + self.colour + ")"

    def rotate_right(self, root):
        # parent = self.parent
        leftChild = self.left

        self.left = leftChild.right

        if None != leftChild.right:
            leftChild.right.parent = self

        leftChild.parent = self.parent

        if None == self.parent:
            root = leftChild
        elif self == self.parent.right:
            self.parent.right = leftChild
        else:
            self.parent.left = leftChild


        leftChild.right = self
        self.parent = leftChild
        
        return root

    def rotate_left(self, root):
        # parent = self.parent
        rightChild = self.right

        self.right = rightChild.left

        if None != rightChild.left:
            rightChild.left.parent = self

        rightChild.parent = self.parent

        if None == self.parent:
            root = rightChild
        elif self == self.parent.left:
            self.parent.left = rightChild
        else:
            self.parent.right = rightChild

        rightChild.left = self
        self.parent = rightChild

        return root
                    
        

class RBTree:

    def __init__(self,):
        self.root = None

    def is_empty(self,):
        return self.root == None

    def get_height(self,):
        if self.is_empty():
            return 0
        return self.__get_height(self.root)

    def __get_height(self, node):
        if node == None:
            return 0
        return 1 + max(self.__get_height(node.left), self.__get_height(node.right))

    def insert(self, value):
        if self.is_empty():
            self.root = RBNode(value)
            self.root.make_black()
        else:
            self.__insert(self.root, value)

    def __insert(self, node, value):
        if value < node.value:
            if node.left == None:
                node.left = RBNode(value)
                node.left.parent = node
                self.fix(node.left)
            else:
                self.__insert(node.left, value)
        else:
            if node.right == None:
                node.right = RBNode(value)
                node.right.parent = node
                self.fix(node.right)
            else:
                self.__insert(node.right, value)

    def fix(self, node):
        parent = node.parent

        if None == parent:
            node.make_black()
            return
        
        if parent.is_black():
            return
        
        grandparent = parent.parent
        
        if None == grandparent:
            parent.make_black()
            return

        uncle = node.get_uncle()
        
        if None != uncle and uncle.is_red():
            parent.make_black()
            grandparent.make_red()
            uncle.make_black()
            
            self.fix(grandparent)
        elif grandparent.left == parent:
            if parent.right == node:
                self.root = parent.rotate_left(self.root)
                parent = node

            self.root = grandparent.rotate_right(self.root)
            
            parent.make_black()
            grandparent.make_red()
        else:
            if parent.left == node:
                self.root = parent.rotate_right(self.root)
                parent = node
            
            self.root = grandparent.rotate_left(self.root)
            
            parent.make_black()
            grandparent.make_red()
        
    def __str__(self):
        if self.is_empty():
            return "[]"
        return "[" + self.__str_helper(self.root) + "]"

    def __str_helper(self, node):
        if node.is_leaf():
            return "[" + str(node) + "]"
        if node.left == None:
            return "[" + str(node) + " -> " + self.__str_helper(node.right) + "]"
        if node.right == None:
            return "[" +  self.__str_helper(node.left) + " <- " + str(node) + "]"
        return "[" + self.__str_helper(node.left) + " <- " + str(node) + " -> " + self.__str_helper(node.right) + "]"
    
    def print_tree(self):
        self.__print_helper(self.root, "", True)
        
    
    def __print_helper(self, node, indent, last):
        if node != None:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "

            s_color = "RED" if node.is_red() else "BLACK"
            print(str(node.value) + "(" + s_color + ")")
            self.__print_helper(node.left, indent, False)
            self.__print_helper(node.right, indent, True)


class BST:

    def __init__(self,):
        self.root = None

    def is_empty(self,):
        return self.root == None

    def get_height(self,):
        if self.is_empty():
            return 0
        return self.__get_height(self.root)

    def __get_height(self, node):
        if node == None:
            return 0
        return 1 + max(self.__get_height(node.left), self.__get_height(node.right))

    def insert(self, value):
        if self.is_empty():
            self.root = RBNode(value)
            self.root.make_black()
        else:
            self.__insert(self.root, value)

    def __insert(self, node, value):
        if value < node.value:
            if node.left == None:
                node.left = RBNode(value)
                node.left.parent = node
            else:
                self.__insert(node.left, value)
        else:
            if node.right == None:
                node.right = RBNode(value)
                node.right.parent = node
            else:
                self.__insert(node.right, value)


def generateList(length):
    return [random.randint(1, 100000) for _ in range(length)]

def experiment(length):
    myList = generateList(length)

    rbTree = RBTree()
    bst = BST()

    for item in myList:
        rbTree.insert(item)
        bst.insert(item)

    rbTreeHeight = rbTree.get_height()
    bstHeight = bst.get_height()

    return rbTreeHeight, bstHeight


def runExperiments(numExperiments, listLength):
    rbTreeHeights = []
    bstHeights = []

    for _ in range(numExperiments):
        rbTreeHeight, bstHeight = experiment(listLength)
        rbTreeHeights.append(rbTreeHeight)
        bstHeights.append(bstHeight)

    return rbTreeHeights, bstHeights

def plotGraph(rbTreeHeights, bstHeights, listLength):
    plt.plot(rbTreeHeights, label='Red-Black Tree')
    plt.plot(bstHeights, label='Binary Search Tree')
    plt.xlabel('Experiment')
    plt.ylabel('Tree Height')
    plt.title(f'Tree Heights for List of Length {listLength}')
    plt.legend()
    plt.show()


numExperiments = 5
listLength = 10000

rbTreeHeights, bstHeights = runExperiments(numExperiments, listLength)
plotGraph(rbTreeHeights, bstHeights, listLength)