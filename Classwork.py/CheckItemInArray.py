Array = [1,2,3,4,5,6,7,8,9,10]

search = (input("Input a number to check if it is in the list: "))

for i in range (len(Array)):
    if search in str(Array[i]):
        print("Yes, in position " + str(i+1))

