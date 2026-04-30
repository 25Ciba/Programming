numbers= [0]*6
total=0
n =len(numbers)

for  i in range(n):
    numbers[i] = input("Number:")
#
for i in range(n-1,-1,-1):
    print(numbers[i])
#
for i in range(n):
    total = total + int(numbers[i])
#
print("Total: ", total)
avg = total/n
print("Average: ", avg)