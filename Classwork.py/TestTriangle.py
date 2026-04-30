while True:
    length_1 = int(input("Enter whole number 1-1000: "))
    length_2 = int(input("Enter whole number 1-1000: "))
    length_3 = int(input("Enter whole number 1-1000: "))
    print("Entered values:", f"{length_1}, {length_2} , {length_3} ")

    #Sort tem into ascending order
    variable_list = (length_1, length_2, length_3)
    list1 = sorted(variable_list)
    length_1 = list1[0]
    length_2 = list1[1]
    length_3 = list1[2]

    #use exit for invalid lengths less than 0 or more than 1000
    if int(length_1) < 1 or int(length_1) >1000:
        exit("All of the sides need to within the range 1-1000")
    if int(length_2) < 1 or int(length_2) >1000:
        exit("All of the sides need to within the range 1-1000")
    if int(length_3) < 1 or int(length_3) > 1000:
        exit("All of the sides need to within the range 1-1000")

    #if triangle is equilateral sides are all equal
    if (length_1 >= length_2 + length_3) or (length_2 >= length_1 + length_3) or (length_3 >= length_1 + length_2):
        print("triangle is impossible")

    elif length_1 == length_2 == length_3:
        print("Triangle is equilateral")

    #right angled triangle a**2+b**2=c**2
    elif int(length_1)**2 + int(length_2)**2 == int(length_3)**2:
        print("Triangle is right angled")

    #if triangle is isosceles 2 sides are equal
    elif length_1 == length_2 or length_2 == length_3 or length_1 == length_3:
        print("Triangle is isosceles")

    #using else to say triangle is scalene
    else:
        print("Triangle is scalene")
    
    # HERONS FORUMLA TO CALC AREA TS
    s = (sum(list1)/2)
    print(s)
    area = ((s*(s-length_1)*(s-length_2)*(s-length_3))**0.5)
    print(f"Your area is {area}")