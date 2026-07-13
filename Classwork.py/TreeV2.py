tree = [
    [1, 24, 3],
    [5, 15, 2],
    [-1, 17, -1],
    [4, 38, 6],
    [-1, 29, -1],
    [-1, 9, -1],
    [-1, 58, -1],
]

tree_ = [
    [1, "F", 2],
    [3, "D", -1],
    [4, "H", 5],
    [6, "B", 7],
    [-1, "G", -1],
    [-1, "J", 8],
    [-1, "A", -1],
    [-1, "C", -1],
    [-1, "Z", -1],
]


#========================

#Tree

def preOrder(p):
    print(tree[p][1]) #
    if tree[p][0] != -1:
        preOrder(tree[p][0])
    if tree[p][2] != -1:
        preOrder(tree[p][2])

def inOrder(p):
    if tree[p][0] != -1:
        inOrder(tree[p][0])
    print(tree[p][1])  #
    if tree[p][2] != -1:
        inOrder(tree[p][2])

def postOrder(p):
    if tree[p][0] != -1:
        postOrder(tree[p][0])
    if tree[p][2] != -1:
        postOrder(tree[p][2])
    print(tree[p][1])  #

#==============================
#tree_

def preOrder_(p):
    print(tree_[p][1]) #
    if tree_[p][0] != -1:
        preOrder_(tree_[p][0])
    if tree_[p][2] != -1:
        preOrder_(tree_[p][2])

def inOrder_(p):
    if tree_[p][0] != -1:
        inOrder_(tree_[p][0])
    print(tree_[p][1])  #
    if tree_[p][2] != -1:
        inOrder_(tree_[p][2])

def postOrder_(p):
    if tree_[p][0] != -1:
        postOrder_(tree_[p][0])
    if tree_[p][2] != -1:
        postOrder_(tree_[p][2])
    print(tree_[p][1])  #

#===================================

preOrder(0)
print("--------------")
inOrder(0)
print("--------------")
postOrder(0)

#----
print("NOW ON ARRAY 2")
#----

preOrder_(0)
print("--------------")
inOrder_(0)
print("--------------")
postOrder_(0)

#===================================