#A tuple is an ordered sequence of elements that is immutable, 
#which means that the values within the tuple cannot be modified when the program is running. 
#The elements of a tuple can be of different data types, e.g. a mix of strings and integers.
#A tuple is a useful way of grouping and organising data items to make them easier to access and use. 
#A tuple can be used to return multiple values from a function. Similarly, 
#a tuple can be used to group together a set of disparate items to be passed into a procedure or function. 
#Results from SQL queries are often received as tuples.
#Elements of tuples are accessed by position (index) in the same way that you access elements of an array.

#==================================

#Suppose you are creating a computer game and you want to allow the player to be able to pause and resume play at any time. 
#When the game is paused, you must store the game data so that the game can be restarted where it was left off. 
#A tuple could be used to collect together the data and then it could be written in a single operation to a binary file. 
#When the player wished to pick up a game, the data could be loaded and the items read from the tuple into the relevant structures of the game. 
#This process is shown in pseudocode below. 

#==================================

# This is written in Pseudo Code

TUPLE game_data(4)  // Declare a tuple of 4 elements
game_data = (grid, score, inventory, player_position)  // Assign data to the tuple
game_file = OPEN_WRITE("explorer.bin")  // Open a binary file for writing
game_file.WRITEALL(game_data, game_file)  // Write the game data to the file
game_file.CLOSE()  // Close the file

#==================================