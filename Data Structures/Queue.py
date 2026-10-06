MAX_SIZE = 100 
queue = []
front = 0
rear = -1

###

def is_full(rear):
    if rear + 1 == MAX_SIZE:
        return True
    else:
        return False

#

def is_empty(front, rear):
    if front > rear:
        return True
    else:
        return False

#

def enqueue(queue, rear, data):
    if is_full(rear) == True:
        print(f"\nQueue is full - {data} not added")
    else:          
        rear = rear + 1
        queue[rear] = data
    return rear

#

def dequeue(queue, front, rear):
    if is_empty(front, rear) == True:
        print("\nQueue is empty - nothing to dequeue")
        dequeued_item = None
    else:
        dequeued_item = queue[front]
        front = front + 1
    return dequeued_item, front