MAX_SIZE = 100  # Use a constant
stack = []
top = -1

###

def is_full(top):
    if top == MAX_SIZE - 1:
        return True
    else:
        return False

#

def is_empty(top):
    if top == -1:
        return True
    else:
        return False

#

def push(stack, top, data):
    if is_full(top) == True:
        print(f"Stack is full - {data} not added")
    else:
        top = top + 1
        stack[top] = data
    return top

#

def pop(stack, top):
    if is_empty(top) == True:
        print("\nStack is empty - nothing to pop")
        popped_item = None
    else:
        popped_item = stack[top]
        top = top - 1
    return popped_item, top 

#

def peek(stack, top):
    if is_empty(top):
        print("Stack is empty - nothing to peek")
        peeked_item = None
    else:
        peeked_item = stack[top]
    return peeked_item