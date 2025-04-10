def X():
    angle = int(input("Ingrese un ángulo objetivo: "))
    return angle

def Y():
    distance = int(input("Ingrese una distancia objetivo: "))
    return distance

def s1():
    sensor1 = int(input("Simule distancia actual: "))
    return sensor1

def s2():
    sensor2 = int(input("Simule ángulo actual: "))
    return sensor2

def s3():
    sensor3 = int(input("Simule ultrasónico: "))
    return sensor3

# Lista para representar el arreglo board[3]
board = [0, 0, 0]

def boardSens():
    board[0] = s1()
    board[1] = s2()
    board[2] = s3()

def getboardSens(x):
    if x == 1:
        return board[0]
    elif x == 2:
        return board[1]
    elif x == 3:
        return board[2]
    else:
        return None

def C1():
    print("ACCION: Parado")
    print("-------------------------------------")

def C2():
    print("ACCION: Avanza por 0.5 sec")
    print("-------------------------------------")

def C3():
    print("ACCION: Giro a la Der. por 0.5 sec")
    print("-------------------------------------")

def C4():
    print("ACCION: Giro a la Izq. por 0.5 sec")
    print("-------------------------------------")

def C5():
    print("ACCION: Set valores de Saux y S1")
    print("-------------------------------------")

def boardComp(comp):
    if comp == 1:
        C1()
    elif comp == 2:
        C2()
    elif comp == 3:
        C3()
    elif comp == 4:
        C4()
    elif comp == 5:
        C5()

def main():
    x = X()       # Ángulo objetivo
    y = Y()       # Distancia objetivo

    while True:
        print("*********************************")
        print("DATOS INICIALES")
        boardSens()
        print("*********************************")
        saux = getboardSens(2) + x  # Saux = S2 + X

        while True:
            print("DATOS ACTUALES")
            boardSens()
            print("-------------------------------------")
            if getboardSens(3) == 1:  # S3 == 1 significa obstáculo detectado
                C1()
                C4()
                break
            else:
                if getboardSens(2) == saux:  # S2 == Saux
                    if getboardSens(1) == y:  # S1 == Y
                        C1()
                        C5()
                        break
                    else:
                        C2()
                else:
                    if (saux - getboardSens(2)) > 0:
                        C4()
                    else:
                        C3()

if __name__ == "__main__":
    main()