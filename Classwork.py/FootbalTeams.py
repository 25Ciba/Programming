global teams, scores

teams = ["Arsenal", "Aston Villa", "Chelsea", "Liverpool", "Manchester City", "Manchester United", "Newcastle United", "Nottingham Forest", "Tottenham Hotspur", "Everton"]
scores = [0,0,0,0,0,0,0,0,0,0]

###

def ShowScores():
    for i in range(len(scores)):
        print(scores[i])

###

def ShowTeams():
    for i in range(len(teams)):
        print(teams[i])
        print(" ")

###

def AddpointsMatch():
    global scores, teams
    for i in range (len(teams)):
        points = int(input(f"Enter points for {teams[i]}: "))
        print(" ")
        scores[i] = points

###

def ShowTeamANDScores():
    global scores, teams
    for i in range (len(teams)):
        print(teams[i],scores[i])

###

def HighestScore():
    global teams, scores
    i = 0
    Highest = scores[i]
    for i in range(len(scores)-1):
        if scores[i-1] >= Highest:
            Highest = scores[i-1]
            team = teams[i-1]
    print(f"Top Score out of all ten teams: {team} with {str(Highest)} points.")
    print(" ")

###

def alphatbetSort():
    



AddpointsMatch()
HighestScore()
