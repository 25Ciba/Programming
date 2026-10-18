maxsize = 100
kBuffer = [None] * maxsize
front = -1
rear = -1
size = 0

###

def is_empty(size):

    if size == 0:
        return True
    else:
        return False

#

def is_full(size):

    if size == maxsize:
        return True
    else:
        return False

#

def dequeue(kBuffer, front, rear, size):

    if is_empty(size) == True:
        print("\nQueue is empty - nothing to dequeue")
        dequeued_item = None
    else:
        dequeued_item = kBuffer[front]
        kBuffer[front] = None
        if front == rear:
            front = -1
            rear = -1
        else:
            front = (front + 1) % maxsize
        size = size - 1
    return dequeued_item, front, rear, size

#

def enqueue(kBuffer, front, rear, size, data):

    if is_full(size) == True:
        print(f"\nQueue is full - {data} not added")
    else:
        rear = (rear + 1) % maxsize
        kBuffer[rear] = data
        if front == -1:
            front = 0
        size = size + 1
    return front, rear, size

#