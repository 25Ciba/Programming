#-----------------------------------------

class Node():

    # Constructor
    def __init__(self, theValue):
        self.value = theValue
        self.nextNode = None

    # Getters
    def getValue(self):
        return self.value

    def getNextNode(self):
        return self.nextNode

    # Setters
    def setValue(self,newValue):
        self.value = newValue
    
    def setNextNode(self, newNode):
        self.nextNode = newNode

#-----------------------------------------

# Instantiate Nodes
node1 = Node("Bob")
node2 = Node("Tony")
node3 = Node("Ivan")
node4 = Node("Matt")
node5 = Node("Jahmai")

#-----------------------------------------

# # Print Nodes
# print(node1)
# print(node2)
# print(node3)
# print(node4)
# print(node5)

#------------------------------------------

# Set headpointer to next node up to node 5
headpointer = node1
headpointer.setNextNode(node2)
headpointer.getNextNode().setNextNode(node3)
headpointer.getNextNode().getNextNode().setNextNode(node4)
headpointer.getNextNode().getNextNode().getNextNode().setNextNode(node5)

#------------------------------------------

#  Print all up to node 5
#print(headpointer.getValue())
#print(headpointer.getNextNode().getValue())
#print(headpointer.getNextNode().getNextNode().getValue())
#print(headpointer.getNextNode().getNextNode().getNextNode().getValue())
#print(headpointer.getNextNode().getNextNode().getNextNode().getNextNode().getValue())

#-------------------------------------------

# traverse the list (but not in a procedure)
current = headpointer
while current != None:
    print(current.getValue())
    current = current.getNextNode()

#-------------------------------------------