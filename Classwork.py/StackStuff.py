Stack = ["","","","",""]
Top = 0
Size = 0

#================#

#Because im lazy

def add():
    top = top+1
    size = size+1 

def remove():
    top = top-1
    size = size-1

#=================#

def push(item):
    global top
    Stack(top) = item
    add()

def pop():

    remove()

#global topand size
#Top changes based on size but size dictates if it isa free or not