Cards = [1,6,7,9,2,4,5,8]

swap = True
num = 1
while swap:
    swap = False
    for i in (range(len(Cards)-num)):
        if Cards[i] > Cards[i+1]:
            temp = Cards[i]
            Cards[i] = Cards[i+1]
            Cards[i+1] = temp
            print("Swap")
            swap = True
    print(Cards)
    num = num+1

