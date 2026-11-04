answers = [
    [True, False, False],
    [False, True, False],
    [False, False, True],
    [False, False, True],
    [False, True, False],
    [False, True, False],
    [True, False, False]
]

#print which one is chosen the most.
#print how many times it was chosen.

############################################

CountA = 0
CountB = 0
CountC = 0

for i in range(answers):
    if answers[i][0] == True:
        CountA += 1
    elif answers[i][1] == True:
        CountB += 1
    elif answers[i][2] == True:
        CountC +=1

if CountA > CountB and CountA > CountB:
    print(CountA)
if CountA > CountB and CountA > CountB: #ect
    print(CountA)
if CountA > CountB and CountA > CountB: #ect
    print(CountA)