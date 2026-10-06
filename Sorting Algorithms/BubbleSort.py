def Bubble_Sort_For_Loops_Only(items):

    num_items = len(items)
    for pass_num in range(1, num_items):
        for index in range(0, num_items - 1):
            if items[index] > items[index + 1]:
                temp = items[index]
                items[index] = items[index + 1]
                items[index + 1] = temp

#

def Bubble_Sort_While_AND_For_Loops(items):

    num_items = len(items)
    swapped = True
    pass_num = 1

    while swapped == True:
        swapped = False
        for index in range(0, num_items - pass_num):
            if items[index] > items[index + 1]:
                temp = items[index]
                items[index] = items[index + 1]
                items[index + 1] = temp
                swapped = True
        pass_num = pass_num + 1