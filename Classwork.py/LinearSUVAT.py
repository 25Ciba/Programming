import math

#---------------------------------------------------------------------------

def LinearSUVAT():
    print("Please input the values which you are aware of. If you do not have a value for this then please type 'NA'. ")
    u = int(input("Please input initial velocity. U: "))
    v = int(input("Please input final velocity. V: "))
    s = int(input("Please input horizontal distance. S: "))
    a = int(input("Please input the acceleration. a: "))
    t = int(input("Please input time taken. t: "))
    solve = input("Please input what value you would like to find now but in capitals. (eg type S,U,V,A,T) : ")
    if solve == 'S':
        if a == 'NA' and s == 'NA':
            s = (0.5(u + v)*t)
            print(s)
        elif u == 'NA' and s == 'NA':
            s = ((v*t)+(-0.5((a)(t**2))))
            print(s)
        elif v == 'NA' and s == 'NA':
            s = ((u*t)+(0.5((a)(t**2))))
            print(s)
        elif t == 'NA' and s == 'NA':
            s = (((u**2)+(v**2)) / (2*a))
            print(s)
    elif solve == 'U':
        if u == 'NA' and 
        
         
        


# Determine the axis ( x, y, right , left)
# I need to identify the positive direction
# Make sure a = contant
# 

#---------------------------------------------------------------------------

################
# Main Program #
################

print("This program will assume to take the value of g when in vertical axis. (Value of g is 9.81 - sorry maths students).")
direction = input("Please input whether you are in the vertical or horizontal axis. Type 'V' or 'H' respectively: ")

# Horizontal
if direction == 'H':
    a = 9.81

else:
    sign = input("Please select whether 'Up' or 'Down' will be seen as positive. (type 'Up' or 'Down') : ")
    # Up is +
    if sign == 'Up':
        a = a*-1

    # Down is +
    else:
        a = a
    
s = (0.5(u + v)*t) # no s or  a
s = ((v*t)+(-0.5((a)(t**2)))) # vt - no s or u
s = ((u*t)+(0.5((a)(t**2)))) # ut - no s or v
s = (((u**2)+(v**2)) / (2*a))

v = u - a*t

u = v - a*t # no u no s
u = ((s/t) + ((-0.5*a)*t)) # no u no v
