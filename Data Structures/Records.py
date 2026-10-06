#==================================
#DEFINING AND USING

class PlayerRecord():
    
    def __init__ (self):
        self.player_number = None
        self.first_name = None
        self.last_name = None
        self.date_of_birth = None
        self.position = None
        self.injured = None

#===================================
#CREATE A RECORD TO STORE THE DETAILS

# Create a new player record
player1 = PlayerRecord()

# Store the details of the player
player1.player_number = 1
player1.first_name = "Maria"
player1.last_name = "Oarps"
player1.date_of_birth = datetime.datetime(1994, 7, 3)
player1.position = "Goalkeeper"
player1.injured = False

#===================================
#TO RETRIVE INFO ABT PLAYER, YOU MUST SPECIFY
# - THE NAME OF RECORD AND FIELD YOU NEED.

# Display the player's name and position
print(f"Name: {player1.first_name} {player1.last_name}")
print(f"Position: {player1.position}")