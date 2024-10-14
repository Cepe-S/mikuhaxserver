newToken = input("Ingrese el nuevo token: ").strip()

if (len(newToken) == 39 and newToken[4] == '.'):
    with open("files/token.txt", "w") as file:
        file.write(newToken)