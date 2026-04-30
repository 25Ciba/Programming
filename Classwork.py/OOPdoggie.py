class Dog():
    
    #private attributes identified with _
    #constructor
    
    def __init__(self, theName, theColour):
        self._name = theName
        self._colour = theColour
        self._age = 0
    
    #Getter methods

    def getName(self):
        return self._name

    def getColour(self):
        return self._colour
    
    def getAge(self):
        return self._age

    #Setter methods

    def setName(self, newName):
        self._name = newName

    def setColour(self, newColour):
        self._colour = newColour

    def setAge(self, newAge):
        self._age = newAge

###### MAIN PROGRAM ######

myDog1 = Dog("Ghost", "White")
myDog2 = Dog("Fletcher", "Brown")
myDog3 = Dog("Dexter", "Unknown")

#get colour of dog
def colourOfDog():
    dogColour = myDog3.getColour()

    #check if colour is = unknown
        #if yes get new input 
        #set the colur

    if dogColour == "Unknown":
        newColour = input("Enter Colour of Dog: ")
        myDog3.setColour(newColour)

    #output the name and colour of the dog

    print("Name: "+myDog3.getName()+", "+myDog3.getColour())

#Check Dog Age

def checkDogAge(aDog):
    if aDog.getAge() < 3:
        print("Get their medication")
    elif aDog.getAge() > 10:
        print("Might wanna get a new Dog.")