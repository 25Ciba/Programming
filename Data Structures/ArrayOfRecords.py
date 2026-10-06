#===================================

import datetime

#Python does not have built-in support for arrays. 
#Instead you can use a list to replicate some of the same functionality.
#Notice that an empty list in Python is declared using square brackets [], 
# and a size is not given since a list is a dynamic data structure. 
#The append command is used to add an element to the end of the list, starting at index 0.

def main():
    
    # Declare a list to store the player records
    first_team = []

    # Testing - create 4 players and add them to the list
    player1 = create_player(1, "Maria", "Oarps", 3, 7, 1994, "Goalkeeper", False)
    first_team.append(player1)
    player2 = create_player(2, "Lucie", "Gold", 18, 10, 1991, "Defender", True)
    first_team.append(player2)
    player3 = create_player(3, "Raquel", "Weekly", 12, 6, 1992, "Defender", False)
    first_team.append(player3)
    player4 = create_player(4, "Kiera", "Welsh", 4, 8, 1998, "Midfielder", False)
    first_team.append(player4)

#===================================


#To use the datetime object in Python, you will need to import
# a module with the same name by adding the following statement to the top of your program:
# import datetime 

def create_player(p_number, f_name, l_name, day, month, year, pos, inj):

    # Create a new player record
    player = PlayerRecord()

    # Store the details of the player
    player.player_id = p_id
    player.first_name = f_name
    player.last_name = l_name
    player.date_of_birth = datetime.datetime(year, month, day)
    player.position = pos
    player.injured = inj

    # Return the player record
    return player

#===================================

#To output the details of each player,
# you can iterate over each record in the first_team array and access
# the fields of each record. An example of this is shown below: 

def display_players(players_list):  

    # Repeat for each player in the players list of records
    for player in players_list:

        # Display the player's number, name and position
        print(f"\nNumber: {player.player_number}")
        print(f"Name: {player.first_name} {player.last_name}")
        print(f"Position: {player.position}")

#===================================