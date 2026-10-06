#===================================

class Node():

    #Constructor
    def __init__(self, given_data):
        self.data = given_data
        self.next = None

    #methods

    def get_data(self):
        return self.data

    def get_next(self):
        return self.next

    def set_next(self, new_next):
        self.next = new_next

class LinkedList():

    #Constructor
    def __init__(self):

        self.head = None

    #Methods

    def traverse(self):  
        current = self.head
    while current is not None:
        print(current.get_data())
        current = current.get_next()

    #

    def insert_at_front(self, data):

        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            new_node.set_next(self.head)            
            self.head = new_node

    #

    def insert_in_order(self, data):

        new_node = Node(data)
        current = self.head
        if current is None:
            self.head = new_node
        elif new_node.get_data() < current.get_data():
            new_node.set_next(self.head)
            self.head = new_node
        else:
            while (current.get_next() is not None
                  and current.get_next().get_data() < new_node.get_data()):
                current = current.get_next()
            new_node.set_next(current.get_next())
            current.set_next(new_node)

    #

    def delete(self, data):
        
        current = self.head
        if current.get_data() == data:
            self.head = current.get_next()
        else:
            while current.get_next().get_data() != data:
                current = current.get_next()
            current.set_next(current.get_next().get_next())

    #
        
#===================================

def traverse(my_list):

    current = my_list.head
    while current is not None:
        print(current.data)
        current = current.next

#===================================

# Instantiate an empty linked list object
my_list = LinkedList()


