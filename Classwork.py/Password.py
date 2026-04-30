def getPword(attempt):
    if attempt == 1:
        respond = "Enter password: "
    else:
        respond = "Enter password again: "

    password = input(respond)

    while len(password) < 6 or len(password) > 8:
        print("Error. password must be 6 to 8 characters long")
        if attempt == 1:
            password = input("Enter password: ")
        else:
            password = input("Enter password again: ")
    return password

while True:
    pword1 = getPword(1)
    pword2 = getPword(2)

    if pword1 != pword2:
        print("Error: passwords do not match")
    else:
        break

print("Password change successful")