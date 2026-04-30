Grid = [
    ["x","x","x","x"],
    ["x","x","x","x"],
    ["x","x","x","x"],
    ["x","x","x","x"],
    ["x","x","x","x"],
    ["x","x","x","x"],
]

def printgrid():
    for i in range(len(Grid)):
        for j in range(len(Grid[i])):
            print(Grid[i][j], end=" | ")
        print()


def inputmove():
    row = int(input("Enter a  row to move to(1-6): "))
    collum = int(input("Enter a  collum to move to(1-4): "))
    for i in range(len(Grid)):
            for j in range(len(Grid[i])):
                if Grid[i][j] == "O":
                    Grid[i][j] = "x"
                    Grid[row - 1][collum - 1] = "O"
                    printgrid()
                    return

printgrid()
while True:
    inputmove()