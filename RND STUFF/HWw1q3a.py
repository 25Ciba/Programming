global Medal
Medal = [4,7,1,3]
School = ["AAAA", "BBBB", "CCCC", "DDDD"]
while True:
    SchoolNumber = int(input(("Please enter the School Number (1-A, 2-B ect). If you want to see all results please input -1 : "))) 
    if SchoolNumber == -1:
        print(f"""

        ################### SCORES ###################

        SCHOOL NUMBER  |   SCHOOL NAME   |  No. MEDALS

                |1|           |{School[0]}|          |{Medal[0]}|
        
                |2|           |{School[1]}|          |{Medal[1]}|

                |3|           |{School[2]}|          |{Medal[2]}|

                |4|           |{School[3]}|          |{Medal[3]}|
        
        ##############################################
        
        """)
    elif SchoolNumber == 1:
        MedalAdd = int(input(f"Please enter the medals won by {School[0]} : ")) 
        Medal[0] = MedalAdd
        print(Medal)
    elif SchoolNumber == 2:
        MedalAdd = int(input(f"Please enter the medals won by {School[1]} : ")) 
        Medal[1] = MedalAdd
        print(Medal)
    elif SchoolNumber == 3:
        MedalAdd = int(input(f"Please enter the medals won by {School[2]} : ")) 
        Medal[2] = MedalAdd
        print(Medal)
    elif SchoolNumber == 4:
        MedalAdd = int(input(f"Please enter the medals won by {School[3]} : ")) 
        Medal[3] = MedalAdd
        print(Medal)
    else:
        print("Not a valid input Please try again..")
        
        
