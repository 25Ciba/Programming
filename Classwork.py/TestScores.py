def allScores():
    for i in range(len(scores)):
        for j in range(len(scores[0])):
            print(scores[i][j])

def peopleScores():
    for i in range(len(names)):
        print(names[i] + ": " + str(scores[i]))

def valueForPeopleScores():
    for i in range(len(names)):
        print(str(i)+": "+names[i])

def daysOfTheWeek():
    for i in range(len(days)):
        print(str(i)+": "+days[i])

def findIdPerson():
    for i in range(len(names)):
        print(str(i)+": " + names[i])

def findNameScoreAndDay ():
    person = int(input("Enter Person ID: "))
    day = int(input("Enter what day you would like to see: "))

    for i in range(len(names)):
        print(str(names[person]) + " got " + str(scores[person][day]), "on " + str(days[day]))
        break

def findAvgScore():
    person2 = int(input("Enter person Id to find their weekly average: "))
    personAvg = sum(scores[person2])
    personAvgTotal = personAvg / len(scores[person2])
    
    for i in range(len(names)):
            print(str(names[person2]) + "'s average score was " + str(personAvgTotal))
            break  

def allScoresTotalAvg():
    total = 0
    for i in range(len(scores)):
        for j in range(len(scores[0])):
            total += scores[i][j]
    avg = total / len(scores)
    average = avg * 10 / 70
    print("Average overall was; ",average)


def askAvgWeekly():
    askAvgWeekly1 = (input("Would you like you find the total average of all pupils over the week. Type 'Yes' or 'No': "))
    if askAvgWeekly1 == "Yes":
        allScoresTotalAvg()
    else:
        print("Thank you for using my program. It will reset in(...)")

def format():
    print("###############")
    print("               ")
    print("Input these to answer questions.")
    print("_______________")
    print("               ")
    print("ID of students: ")
    print("               ")
    valueForPeopleScores()
    print("               ")
    print("_______________")
    print("               ")
    print("Number for designated day: ")
    print("               ")
    daysOfTheWeek()
    print("               ")
    print("_______________")
    print("               ")

#######################

days = ["Monday", "Teusday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

scores = [
    [33, 45, 37, 62, 71, 25, 46],
    [46, 47, 36, 51, 50, 49, 70],
    [75, 69, 78, 59, 80, 85, 90],
    [25, 28, 39, 31, 50, 41, 28],
    [25, 26, 28, 27, 30, 37, 35],
    [62, 72, 68, 74, 60, 76, 82],
    [72, 84, 51, 68, 65, 62, 79],
    [78, 66, 74, 72, 80, 68, 66],
    [90, 98, 77, 56, 65, 74, 83],
    [72, 84, 33, 56, 54, 60, 78],
]

names = ["Jamai", "Mufed", "Sem", "Richard", "Caleb", "Abeer", "Derin", "Bob", "Atlas", "Cain"]

######################

while True:

    askChoice = int(input('''
What would you like to do? Enter one of the following numbers;

1. Find all scores of all people per day, in a week.

2. Find the score of someone on a specific day in the week.

3. Find the average weekly score of someone.

4. Find the average score of everyone in total across the week. 
                                            
Which one would you like: '''))
    
    from time import sleep
    if askChoice == 1:
        peopleScores()
    sleep(1)

    from time import sleep
    if askChoice == 2:
        format()
        findNameScoreAndDay()
    sleep(1)

    from time import sleep
    if askChoice == 3:
        format()
        findAvgScore()
    sleep(1)

    from time import sleep
    if askChoice == 4:
        askAvgWeekly()
    sleep(1)

    from time import sleep
    if askChoice <1 or askChoice >4:
        print("That is not one of the options....")
    sleep(2)
    
#################