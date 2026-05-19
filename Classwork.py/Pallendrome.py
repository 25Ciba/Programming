Stack = []

def Push(item):
    Stack.append(item)

def reverse(item):
    return item[::-1]

#=====================#

#Get user input
word = input("Enter word: ")

#Enter user input into Stack
for i in range (len(word)):
    Push(word[i])

#Look at Stack
print(Stack)

#Reverse Stack and add to a new list, then check.
Flip = reverse(Stack)
print(Flip)

#Check if it is the same, if not return no.
if Flip == Stack:
    print("This is a pallendrome")
else:
    print("This is not a pallendrome.")
    
from BoardGame import deck

print(deck)