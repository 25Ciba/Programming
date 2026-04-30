########## LINKED LIST CLASS ###########
########################################
########################################
########################################

class LinkedList():
    # constructor
    def __init__(self, headData):
        self.head = Node(headData)

    def getHead(self):
        return self.head

###############

    #Create new procedure using self as a parameter (for the headpointer)
    def traverseList(self):

        #Set current = self.head so we use a variable instead of self.head all the time
        current = self.head 

        # if statements check if the headpointer is pointing to null

        if current == None: #in the case that the headpointer points to null
            print("List is empty")

        else: #the headpointer points to a node (not empty)

            print(current.getData()) #prints the information of/in the node

            while current.getNext() != None: #checks if the next node(using pointer of current node) is empty.
                
                current = current.getNext() #if the next node is not empty, the headpointer points to the next node's pointer

                print(current.getData()) #prints the data of the node the headpointer is NOW looking at

################

    #Create a new procedure using self and data (of the node) for parameters.
    def add(self, data): 
            
            #the data of a node is set to a variable for convenience
            newNode = Node(data)

            #//here i ran into a problem because current wasnt working well so i used self.head//
            #The if statement checks if the headpointer is equal to null.

            if self.head == None: #in the case the headpointer IS equal to null

                self.head = newNode #the headpointer is made equal to the new node

                return
            
            #current is used as a variable instead of self.head
            current = self.head

            while current.getNext() != None: #While the next node is not null

                current = current.getNext() #headpointer is set to the pointer of the next node

            current.setNext(newNode) #make a new node where the headpointer is pointing at NOW

###############

    # def remove(self, data):
    #     current = self.head
    #     wordItem = data
    #     if current = wordItem:
    #          #skip not delete technichally

    

    
########## NODE CLASS #################
class Node():
    # constructor
    def __init__(self, data):
        self.data = data
        self.next = None

    def getData(self):
        return self.data
    
    def getNext(self):
        return self.next
    
    def setNext(self, newNext):
        self.next = newNext

#######################################
# MAIN PROGRAM
#######################################

# create a variable to hold the name of first person to put in list
firstPerson = input("What is the first person in your list?: ")

# instantiated a linked list with first person setup
myList = LinkedList(firstPerson)
myList.add("Bob")
myList.add("Bobb")
myList.add("Bokjmijb")
myList.add("Bofgab")
print(myList.traverseList())