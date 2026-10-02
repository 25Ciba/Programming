Numbersyay = [1,6,2,7,8,1,7,9,2,45,78,23,5,6]
print(Numbersyay)
swap = True
while swap == True:
    swap = False
    for i in range(len(Numbersyay)-1):
        temp = Numbersyay[i]
        if temp > Numbersyay[i+1]:
            Numbersyay[i] = Numbersyay[i+1]
            Numbersyay[i+1] = temp
            swap = True
print(Numbersyay)
