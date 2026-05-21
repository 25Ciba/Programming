#stack size 5
#use an array

Stack = ["","","","",""]
top = 0
size = 0

#======================

def increment():
    global top, size
    top = top+1
    size = size +1

def decrement():
    global top, size
    top = top-1
    size = size-1

def push(item):
    if isFull():
        print("Stack full")
    else:
        Stack[top] = item
        increment()

def pop():
    global top, size
    Stack[top-1] 
    decrement()

def isFull():
    if (len(Stack)) == 4:
        return True
    else:
        return False
    
def isempty():
    if (len(Stack)) == 4:
        return True
    else:
        return False
    
#=======================
#Main Program
push("A")
print(Stack)
pop()
print(Stack)