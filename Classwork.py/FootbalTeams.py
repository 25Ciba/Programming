global teams, scores, addpoint, inOrder

teams = ["Arsenal", "Aston Villa", "Chelsea", "Liverpool", "Manchester City", "Manchester United", "Newcastle United", "Nottingham Forest", "Tottenham Hotspur", "Everton"]
scores = [0,0,0,0,0,0,0,0,0,0]
addpoint = []
inOrder =[]


###

def ShowScores():
    for i in range(len(scores)):
        print(scores[i])

###

def ShowTeams():
    for i in range(len(teams)):
        print(teams[i])

###

def UserAddPoints():
    global scores, addpoint
    count = 0
    ShowTeams()
    while count <= 9:
        userAddPoints = int(input("Please enter the points for each team in order of names listed: "))
        addpoint.append(userAddPoints)
        count = count + 1
    scores = addpoint
    print(scores)

###

#Display highest point teams in order

def HighestScore():
    global addpoint, teams, inOrder
    for i in range(1,len(addpoint)):
        inOrder = addpoint[i]
        pos = i-1
        while addpoint[pos] > inOrder and pos >= 0:
            addpoint[pos+1] = addpoint[pos] 
            pos = pos - 1
        addpoint[pos + 1] = inOrder
    print(inOrder)

###

def Try():
    UserAddPoints()
    HighestScore()

###

Try()



