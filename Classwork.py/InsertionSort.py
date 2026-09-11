#First one is safe into a list.
#The nest element is checked for the second iteration with the one below
#Third iteration the new card is checked against all starting from the top card down tot he first.
#NewCard is the next element that needs to be checked and put into the "Sublist"
#This tracks when we can finish and a count control for the next loop/iteration
#This needs to check if the iteration is greater or = to zero (first) and if the iteration aka new card is greater than the current card

Cards = [1,6,7,9,2,4,5,8]

for i in range(1,len(Cards)):
    NewCard = Cards[i]         
    iteration = i - 1          
    while iteration >= 0 and Cards[iteration] > NewCard:   
        Cards[iteration] = Cards[iteration + 1]
        iteration = iteration - 1
    Cards[iteration] = NewCard
print(Cards)
    