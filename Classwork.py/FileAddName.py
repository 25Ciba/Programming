name1 = input("Enter your name: ")
filewrite = open("NameADD.txt", "w")
count = 2
for i in range(9):
    name = input(f"Enter Name {count}: ")
    filewrite.write(name + "\n")
    count = count+1
filewrite.close()
fileread = open("nameADD.txt", "r")
print(fileread.read())
fileread.close()
print("------------")
print("------------")
print("------------")

###

fileToArray = open("NameADD.txt", "r")
Names = []
count = 0
for i in fileToArray:
    j = fileToArray.readline(count)
    Names.append(j)
    count += 1
fileToArray.close()
print(str(Names[i]))



###

# Names = []
# swap = True
# num = 1
# while swap:
#     swap = False
#     for i in (range(len(Names)-num)):
#         if Names[i] > Names[i+1]:
#             temp = Names[i]
#             Names[i] = Names[i+1]
#             Names[i+1] = temp
#             print("Swap")
#             swap = True
#     print(Names + "\n" + "This is now in an array")
#     num = num+1
