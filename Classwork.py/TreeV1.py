tree = [ 
    [1, "A", 2],
    [3, "B", 4],
    [5, "C", -1],
    [-1, "D", 6],
    [-1, "E", -1],
    [-1, "F", -1],
    [-1, "G", -1]
]

def preOrder(p):
    print(tree[p][1])
    if tree[p][0] != -1:
        preOrder(tree[p][0])
    if tree[p][2] != -1:
        preOrder(tree[p][2])
    
def InOrder(p):
    if tree[p][0] != -1:
        InOrder(tree[p][0])
    print(tree[p][1])
    if tree[p][2] != -1:
        InOrder(tree[p][2])

def postOrder(p):
    if tree[p][0] != -1:
        postOrder(tree[p][0])
    if tree[p][2] != -1:
        postOrder(tree[p][2])
    print(tree[p][1])




#============================================================

# Secondtree = [ 
#     {"left": 1, "data": "M", "right": 2},
#     {"left": 3, "data": "H", "right": 4},
#     {"left": 5, "data": "T", "right": 6},
#     {"left": -1, "data": "D", "right": -1},
#     {"left": -1, "data": "K", "right": -1},
#     {"left": -1, "data": "R", "right": -1},
#     {"left": -1, "data": "X", "right": -1},
# ]

# class Node():

#     Thirdtree = [ 
#         {"left": 1, "data": "M", "right": 2},
#         {"left": 3, "data": "H", "right": 4},
#         {"left": 5, "data": "T", "right": 6},
#         {"left": -1, "data": "D", "right": -1},
#         {"left": -1, "data": "K", "right": -1},
#         {"left": -1, "data": "R", "right": -1},
#         {"left": -1, "data": "X", "right": -1},
#     ]

#=============================================================