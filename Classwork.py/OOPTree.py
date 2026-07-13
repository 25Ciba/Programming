class Node():

    #Constructor + Atributes:

    def __init__(self, theData):

        self.data = theData
        self.left = None
        self.right = None

    #Setters and Getters:

        def getData(self):
            print(f"Node Data: {self.data}.")
        
        def setData(self, newData):
            self.data = newData

        #Left

        def getLeft(self):
            return self.left
        
        def setleft(self, newLeft):
            self.left = newLeft
        
        #Right

        def getRight(self):
            return self.right
        
        def setRight(self, newRight):
            self.right = newRight
    
#=========

class LinkedList():
    def __init__(self):
    #No atributes - weird

    #Traversing Functions:

        def preOrder(p):
            print(theTree.getData())
            if theTree.getLeft() != None:
                preOrder(theTree.getLeft())
            if theTree.getRight() != None:
                preOrder(theTree.getRight())

        def inOrder(p):
            if theTree.getLeft() != None:
                inOrder(theTree.getLeft())
            print(theTree.getData())
            if theTree.getRight() != None:
                inOrder(theTree.getRight())

        def postOrder(p):
            if theTree.getLeft() != None:
                postOrder(theTree.getLeft())
            if theTree.getRight() != None:
                postOrder(theTree.getRight())
            print(theTree.getData())

#Need to go through and add the Nodes into List?
theTree = LinkedList()

