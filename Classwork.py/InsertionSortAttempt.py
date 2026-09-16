Cards = [5,9,1,0,2,4,7,2,7,4,5,5,6,0,1]

for i in range(1,len(Cards)):
    NewCard = Cards[i]
    pos = i-1
    while Cards[pos] > NewCard and pos >= 0:
        Cards[pos+1] = Cards[pos] 
        pos = pos - 1
    Cards[pos + 1] = NewCard
print(Cards)


