import random
def NormalMode():
    global num1
    num1 = str(random.randint(1000,10000))

def HardMode():
    global num2
    num2 = str(random.randint(10000,100000))

#
guesscount = 0
#

def Exit1():
    if guess1 == "Exit":
        print("Nice Try. The 4 digit number was: ", num1)

def Exit2():
    if guess2 == "Exit2":
        print("Nice Try. The 5 digit number was: ", num2)

#

def guessnum1():
    global guess1
    guess1 = (input("Guess the 4 digit number: "))

def guessnum2():
    global guess2
    guess2 = (input("Guess the 5 digit number: "))

#

def OneRight1():
    if guess1[0] == num1[0]:
        print("You a got digit correct!")

def TwoRight1():
    if guess1[1] == num1[1]:
        print("You a got digit correct!")

def ThreeRight1():
    if guess1[2] == num1[2]:
        print("You a got digit correct!")

def FourRight1():
    if guess1[3] == num1[3]:
        print("You a got digit correct!")

def Correct1():
    if guess1 == num1:
       print("YOU GOT IT! You got a score of ", guesscount, " guesses. Better luck next time :(")

#

def OneRight2():
    if guess2[0] == num2[0]:
        print("You a got digit correct!")

def TwoRight2():
    if guess2[1] == num2[1]:
        print("You a got digit correct!")

def ThreeRight2():
    if guess2[2] == num2[2]:
        print("You a got digit correct!")

def FourRight2():
    if guess2[3] == num2[3]:
        print("You a got digit correct!")

def FiveRight2():
    if guess2[4] == num2[4]:
        print("You a got digit correct!")

def Correct2():
    if guess2 == num2:
        print("YOU GOT IT! You got a score of ", guesscount, " guesses. Good Job")
    
#

def NormalModePlay():
    while True:
        guessnum1()
        print("--------------------------")
        print("                          ")
        OneRight1()
        TwoRight1()
        ThreeRight1()
        FourRight1()
        print("--------------------------")
        print("                          ")
        Correct1()
        Exit1()

def HardModePlay():
    while True:
        guessnum2()
        print("--------------------------")
        print("                          ")
        OneRight2()
        TwoRight2()
        ThreeRight2()
        FourRight2()
        FiveRight2()
        print("--------------------------")
        print("                          ")
        Correct2()
        Exit2()
        

###########

while True:
    ask = input('''Choose which gamemode you would like to play?
                
    Enter '1' to choose Normal Mode

    Enter '2' to choose Hard Mode

    Please enter an option: ''')

    if ask == "1":
        print("                          ")
        print("At any point you can type 'Exit' to give up and reveal the number. Goodluck!")
        NormalMode()
        guesscount += 1
        NormalModePlay()

    elif ask == "2":
        print("                          ")
        print("At any point you can type 'Exit2' to give up and reveal the number. Goodluck!")
        HardMode()
        guesscount += 1
        HardModePlay()

    else:
        print("                          ")
        print("--------------------------")
        print("                          ")
        print("This is not a suitable option...")
        print("                          ")
        print("--------------------------")
        print("                          ")