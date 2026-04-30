names = ["James", "Cain", "Abigail", "John", "Steven", "Jam"]
#
searchName = input("Enter name to search: ")
for i in range(len(names)):
    if searchName == names[i]:
        print("Person is in this class")
        break
else:
    print("Person not in this class")