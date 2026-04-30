CarPark = [
    [" "," "," "," "," "," ",],
    [" "," "," "," "," "," ",],
    [" "," "," "," "," "," ",],
    [" "," "," "," "," "," ",],
    [" "," "," "," "," "," ",],
    [" "," "," "," "," "," ",],
    [" "," "," "," "," ","X",],
    [" "," "," "," "," "," ",],
    [" "," "," "," "," "," ",],
    [" "," "," "," "," "," ",],
    ]

def emptyCarPark ():
    for i in range (len(CarPark)):
        for j in range ((CarPark)[i]):
            (CarPark)[i][j] == " "

def parkACar ():
    Empty = True
    while Empty == True:

        Row = int(input("What row would you like to park in? "))
        Collum = int(input("What collum would you like to park in? "))

        if (CarPark)[Row - 1][Collum - 1] != " ":
            print("space is not empty.")
            Row = int(input("What row would you like to park in? "))
            Collum = int(input("What collum would you like to park in? "))
            Empty = False

        else:
            CarReg = input("Please enter your car's registration number: ")
            CarPark[Row - 1][Collum - 1] = CarReg
            CarPark.insert(Row -1, Collum - 1)
            print(CarPark)
        break

##################



parkACar()