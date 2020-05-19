import time
from math import sqrt


class Node:
    def __init__(self, name):
        self.name = name
        self.estimation = 0

    #FUNCTIE CARE CALCULEAZA O EURISTICA
    #ACEASTA EURISTICA NU IA IN CONSIDERARE SI RELATIILE DE SUPARARE SI LOCURILE LIBERE, DECI AUTOMAT ARE VALOARE MAI MICA SAU EGALA DECAT COSTUL REAL => ADMISIBILA
    #DIFERENTA DINTRE VALOAREA EURISTICII A UNUI NOD SI CEA A SUCCESORULUI SAU ESTE MEREU 1, DECI ESTE MEREU MAI MICA SAU EGALA DECAT COSTUL REAL, CARE E 1 => CONSISTENTA
    def calculate_estimation1(self):
        # S-A UTILIZAT DISTANTA MANHATTAN
        nrRows = len(matrInput[0])
        rowStart = mapPosition[self.name][1]
        rowFinal = mapPosition[finalInput][1]
        colStart = mapPosition[self.name][0] * 2 + mapPosition[self.name][2]
        colFinal = mapPosition[finalInput][0] * 2 + mapPosition[finalInput][2]

        if rowStart == nrRows - 1:
            val1 = 0
        else:
            val1 = abs(nrRows - rowStart - 2)

        if rowStart == nrRows - 1:
            val2 = 0
        else:
            val2 = abs(nrRows - rowFinal - 2)

        estimation = val1 + val2 + abs(colFinal - colStart)
        return estimation

    #FUNCTIE CARE CALCULEAZA O EURISTICA
    #ACEASTA ESTE MAI MICA DECAT EURISTICA MANHATTAN, CARE ESTE MAI MICA DECAT VALOAREA REALA => ADMISIBILA
    #SE POATE FOLOSI ACELASI ARGUMENT CA LA ADMISIBILITATE; ACEASTA E MAI MICA DECAT CEA MANHATTAN, DECI RESPECTA SI INEGALITATEA => CONSISTENTA
    def calculate_estimation2(self):
        # S-A UTILIZAT DISTANTA EUCLIDIANA

        rowStart = mapPosition[self.name][1]
        rowFinal = mapPosition[finalInput][1]
        colStart = mapPosition[self.name][0] * 2 + mapPosition[self.name][2]
        colFinal = mapPosition[finalInput][0] * 2 + mapPosition[finalInput][2]

        if rowStart == rowFinal:
            estimation = abs(colFinal - colStart)
            return estimation

        difCol = abs(colFinal - colStart)
        difRow = abs(rowFinal - rowStart)
        estimation = sqrt(difCol * difCol + difRow * difRow)
        return estimation

    #FUNCTIE CARE CALCULEAZA O EURISTICA NEADMISIBILA
    def calculate_estimation3(self):
        #EURISTICA NONADMISIBILA

        nrRows = len(matrInput[0])
        rowStart = mapPosition[self.name][1]
        deskStart = mapPosition[self.name][2]

        estimation = 1000 * nrRows * nrRows
        if rowStart == nrRows - 1:
            estimation = 5000 * nrRows * nrRows
        if deskStart == 1 and rowStart == nrRows - 2:
            estimation = 10000 * nrRows * nrRows
        return estimation

    #FUNCTIE CARE DETERMINA LISTA DE SUCCESORI
    def expand(self, parent, whichEstimation):
        # PENTRU FIECARE COPIL AM FACUT O LISTA DE POSIBILI SUCCESORI TINAND CONT DE POZITIA SA IN CLASA SI DE RELATIILE DE SUPARARE
        nrRows = 0
        for i in matrInput:
            nrRows = len(i)
            break
        nodeName = self.name
        listSucc = []
        for i in range(3):
            for j in range(len(matrInput[i])):
                desk = matrInput[i][j]
                for k in range(2):
                    if desk[k] == nodeName:
                        if j != 0:
                            if matrInput[i][j - 1][k] != 'liber':  # VERIFIC COLEGUL DIN FATA
                                deskMates = []
                                deskMates.append(desk[k])
                                deskMates.append(matrInput[i][j - 1][k])
                                deskMatesRev = deskMates[::-1]
                                ok = 1
                                for it in listAngry:
                                    if deskMates == it or deskMatesRev == it:
                                        ok = 0
                                        break
                                if ok == 1:
                                    newNode = Node(matrInput[i][j - 1][k])
                                    if whichEstimation == 1:
                                        newNode.estimation = newNode.calculate_estimation1()
                                    if whichEstimation == 2:
                                        newNode.estimation = newNode.calculate_estimation2()
                                    if whichEstimation == 3:
                                        newNode.estimation = newNode.calculate_estimation3()
                                    newNodeParc = NodeParc(newNode, parent, parent.cost + 1)
                                    listSucc.append(newNodeParc)
                        if j != nrRows - 1:
                            if matrInput[i][j + 1][k] != 'liber':  # VERIFIC COLEGUL DIN SPATE
                                deskMates = []
                                deskMates.append(desk[k])
                                deskMates.append(matrInput[i][j + 1][k])
                                deskMatesRev = deskMates[::-1]
                                ok = 1
                                for it in listAngry:
                                    if deskMates == it or deskMatesRev == it:
                                        ok = 0
                                        break
                                if ok == 1:
                                    newNode = Node(matrInput[i][j + 1][k])
                                    if whichEstimation == 1:
                                        newNode.estimation = newNode.calculate_estimation1()
                                    if whichEstimation == 2:
                                        newNode.estimation = newNode.calculate_estimation2()
                                    if whichEstimation == 3:
                                        newNode.estimation = newNode.calculate_estimation3()
                                    newNodeParc = NodeParc(newNode, parent, parent.cost + 1)
                                    listSucc.append(newNodeParc)
                        # VERIFIC COLEGUL DE PE CEALALTA COLOANA
                        if k == 1:  # CAZUL COLOANA DIN DREAPTA
                            if i != 2:
                                if j == nrRows - 1 or j == nrRows - 2:
                                    if matrInput[i + 1][j][0] != 'liber':
                                        deskMates = []
                                        deskMates.append(desk[k])
                                        deskMates.append(matrInput[i + 1][j][0])
                                        deskMatesRev = deskMates[::-1]
                                        ok = 1
                                        for it in listAngry:
                                            if deskMates == it or deskMatesRev == it:
                                                ok = 0
                                                break
                                        if ok == 1:
                                            newNode = Node(matrInput[i + 1][j][0])
                                            if whichEstimation == 1:
                                                newNode.estimation = newNode.calculate_estimation1()
                                            if whichEstimation == 2:
                                                newNode.estimation = newNode.calculate_estimation2()
                                            if whichEstimation == 3:
                                                newNode.estimation = newNode.calculate_estimation3()
                                            newNodeParc = NodeParc(newNode, parent, parent.cost + 1)
                                            listSucc.append(newNodeParc)
                        if k == 0:
                            if i != 0:  # CAZUL COLOANA DIN STANGA
                                if j == nrRows - 1 or j == nrRows - 2:
                                    if matrInput[i - 1][j][1] != 'liber':
                                        deskMates = []
                                        deskMates.append(desk[k])
                                        deskMates.append(matrInput[i - 1][j][1])
                                        deskMatesRev = deskMates[::-1]
                                        ok = 1
                                        for it in listAngry:
                                            if deskMates == it or deskMatesRev == it:
                                                ok = 0
                                                break
                                        if ok == 1:
                                            newNode = Node(matrInput[i - 1][j][1])
                                            if whichEstimation == 1:
                                                newNode.estimation = newNode.calculate_estimation1()
                                            if whichEstimation == 2:
                                                newNode.estimation = newNode.calculate_estimation2()
                                            if whichEstimation == 3:
                                                newNode.estimation = newNode.calculate_estimation3()
                                            newNodeParc = NodeParc(newNode, parent, parent.cost + 1)
                                            listSucc.append(newNodeParc)
                        if desk[1 - k] != 'liber':  # II VERIFIC COLEGUL DE BANCA
                            deskMates = []
                            deskMates.append(desk[k])
                            deskMates.append(desk[1 - k])
                            deskMatesRev = deskMates[::-1]
                            ok = 1
                            for it in listAngry:
                                if deskMates == it or deskMatesRev == it:
                                    ok = 0
                                    break
                            if ok == 1:
                                newNode = Node(desk[1 - k])
                                if whichEstimation == 1:
                                    newNode.estimation = newNode.calculate_estimation1()
                                if whichEstimation == 2:
                                    newNode.estimation = newNode.calculate_estimation2()
                                if whichEstimation == 3:
                                    newNode.estimation = newNode.calculate_estimation3()
                                newNodeParc = NodeParc(newNode, parent, parent.cost + 1)
                                listSucc.append(newNodeParc)
        return listSucc

    #FUNCTIE DE VERIFICARE A SCOPULUI
    def isFinal(self, final):
        if self.name == finalInput:
            return True
        return False

class NodeParc:
    def __init__(self, node, parent, cost):
        self.node = node
        self.parent = parent
        self.cost = cost
        self.f = self.cost + self.node.estimation

    #FUNCTIE CARE AJUTA LA SORTAREA NODURILOR
    def __lt__(self, other):
        if other.f == self.f:
            if other.cost > self.cost:
                return 0
            else:
                return 1
        elif other.f < self.f:
            return 0
        else:
            return 1

#APLICARE A*
def solve(matrInput, listAngry, startInput, finalInput, whichEstimation, mapPosition):

    #VERIFICAM MAI INTAI DACA ARE VECINI VALIZI ELEVUL FINAL - OPTIMIZARE
    testf = Node(finalInput)
    testFinal = NodeParc(testf, None, 0)
    listTestFinal = testFinal.node.expand(testFinal, whichEstimation)
    if len(listTestFinal) == 0:
        return []

    start = Node(startInput)
    if whichEstimation == 1:
        start.estimation = start.calculate_estimation1()
    if whichEstimation == 2:
        start.estimation = start.calculate_estimation2()
    if whichEstimation == 3:
        start.estimation = start.calculate_estimation3()
    startNode = NodeParc(start, None, 0)

    '''lists = startNode.node.expand(startNode)

    for i in lists:
        print(i.node.name)
    return'''
    open = []
    closed = []
    open.append(startNode)

    while len(open) != 0:
        open.sort()
        '''print("THIS IS OPEN")
        for i in open:
            print(i.node.name + str(i.node.estimation) + " " + str(i.cost) + " " + str(i.f))
            if i.parent == None:
                print(" none")
            else:
                print(i.parent.node.name)
        print("\n")'''
        ''' print("THIS IS CLOSED")
        for i in closed:
            print(i.node.name + str(i.node.estimation) + " " + str(i.cost))
            if i.parent == None:
                print(" none")
            else:
                print(i.parent.node.name)
        print("AFISAM SUCCESORI")'''
        nodeCurr = open[0]
        #print(nodeCurr.node.name)
        open.remove(nodeCurr)
        closed.append(nodeCurr)

        listSucc = nodeCurr.node.expand(nodeCurr, whichEstimation)

        if nodeCurr.node.isFinal(finalInput):
            #O IAU DIN PARINTE IN PARINTE PENTRU A DETERMINA SIRUL DE ELEVI
            parentList = []
            parentList.append(nodeCurr)
            while nodeCurr.parent is not None:
                parentList.append(nodeCurr.parent)
                nodeCurr = nodeCurr.parent
            parentList.reverse()
            return parentList

        for k in range(len(listSucc)):
            newNodeParc = listSucc[k]
            copyNode = nodeCurr
            exist = 0
            while copyNode.parent is not None:
                if copyNode.parent.node.name == newNodeParc.node.name:
                    exist = 1
                    break
                copyNode = copyNode.parent
            '''print(newNodeParc.node.name + " " +  str(exist) + " " + str(newNodeParc.node.estimation) + " " + str(newNodeParc.cost))
            if newNodeParc.parent == None:
                print(" none")
            else:
                print(newNodeParc.parent.node.name)'''

            if exist == 0:
                exist = 0
                for i in closed:
                    if i.node.name == newNodeParc.node.name:
                        exist = 1
                        if newNodeParc.f < i.f:
                            closed.remove(i)
                            open.append(newNodeParc)
                            '''print("MODIFICARE IN 1")'''
                        break
                if exist == 0:
                    for i in open:
                        if i.node.name == newNodeParc.node.name:
                            exist = 1
                            if newNodeParc.f < i.f:
                                open.remove(i)
                                open.append(newNodeParc)
                                '''print("MODIFICARE IN 2")'''
                            break
                if exist == 0:
                    open.append(newNodeParc)
                    '''print("MODIFICARE IN 3")'''
        '''print("NEXT")
        print("\n")'''
    return []

#FUNCTIE CU CARE DETERMIN SEMNUL DINTRE 2 ELEVI
def verif_sign(first, second):
    secondColumn = 0
    secondRow = 0
    secondDesk = 0
    firstColumn = 0
    firstRow = 0
    firstDesk = 0

    for i in range(3):
        for j in range(len(matrInput[i])):
            desk = matrInput[i][j]
            for k in range(2):
                if desk[k] == first:
                    firstColumn = i
                    firstRow = j
                    firstDesk = k
                if desk[k] == second:
                    secondColumn = i
                    secondRow = j
                    secondDesk = k

    if secondRow > firstRow:
        return 'v'
    elif secondRow < firstRow:
        return '^'
    elif secondRow == firstRow:
        if secondColumn == firstColumn:
            if secondDesk > firstDesk:
                return '>'
            else:
                return '<'
        elif secondColumn > firstColumn:
            return '>>'
        elif secondColumn < firstColumn:
            return '<<'


if __name__ == "__main__":
    t0 = time.time()

    print("EXISTA URMATOARELE FISIERE: ")
    print("1. input_no_solution CARE CONTINE DATE CE NU OFERA O SOLUTIE PROBLEMEI")
    print("2. input_solin_solfin UNDE STAREA INITIALA ESTE SI FINALA")
    print("3. input_3-5 UNDE SOLUTIE ARE UN COST INTRE 3 SI 5")
    print("4. input_higher5 UNDE SOLUTIE ARE UN COST MAI MARE DECAT 5")
    print("SELECTATI NUMARUL DE ORDINE AL FISIERULUI PE CARE DORITI SA REALIZATI ACTIUNI")
    whichFile = ' '
    while True:
        whichFile = input()
        if whichFile in ['1', '2', '3', '4']:
            whichFile = int(whichFile)
            break
        else:
            print("Date invalide. Reincearca")

    print("EXISTA URMATOARELE EURISTICI: ")
    print("1. DISTANTA MANHATTAN")
    print("2. DISTANTA EUCLIDIANA")
    print("3. O EURISTICA NEADMISIBILA")
    print("SELECTATI NUMARUL DE ORDINE AL EURISTICII PE CARE DORITI SA O APLICATI")
    whichEstimation = ' '
    while True:
        whichEstimation = input()
        if whichEstimation in ['1', '2', '3']:
            whichEstimation = int(whichEstimation)
            break
        else:
            print("Date invalide. Reincearca")

    # CITIREA DATELOR SI INTRODUCEREA LOR IN STRUCTURILE DE DATE NECESARE REZOLVARII PROBLEMEI
    # PENTRU A MEMORA POZITIILE ELEVILOR IN CLASA AM FOLOSIT O LISTA CU 3 SUBLISTE REPREZENTAND FIECARE DINTRE CELE 3 COLOANE
    # FIECARE SUBLISTA ARE LA RANDUL EI IN COMPONENTA ALTE SUBLISTE REPREZENTAND RANDURILE
    # FIECARE RAND ESTE DE O FORMA UNEI LISTE [COLEG_1, COLEG_2]
    # LISTA CU RELATII DE SUPARARE E PASTRATA INTR-O LISTA CU SUBLISTE DE FORMA [COLEG_1, COLEG_2]
    matrInput = [[], [], []]
    listAngry = []
    startInput = ''
    finalInput = ''
    task = 0

    file = open('input.txt', 'r')

    if whichFile == 1:
        file.close()
        file = open('input_no_solution.txt', 'r')
    if whichFile == 2:
        file.close()
        file = open('input_solin_solfin.txt', 'r')
    if whichFile == 3:
        file.close()
        file = open('input_3-5.txt', 'r')
    if whichFile == 4:
        file.close()
        file = open('input_higher5.txt', 'r')
    # VOM FOLOSI UN DICTIONAR IN CARE PASTRAM PENTRU FIECARE ELEV COORDONATELE IN SALA(COLOANA, RAND, POZITIE IN BANCA) - OPTIMIZARE(PENTRU A NU CAUTA MEREU IN CALCULAREA EURISTICII)
    mapPosition = {}

    for line in file:
        if line == 'suparati\n':
            task = 1
        if line.__contains__('mesaj'):
            task = 2
        if task == 0:
            listNames = line.split(' ')
            listNames[len(listNames) - 1] = listNames[len(listNames) - 1].rstrip()
            for i in range(3):
                desk = []
                desk.append(listNames[2 * i])
                mapPosition[listNames[2 * i]] = (i, len(matrInput[i]), 0)
                desk.append(listNames[2 * i + 1])
                mapPosition[listNames[2 * i + 1]] = (i, len(matrInput[i]), 1)
                matrInput[i].append(desk)
        if task == 1 and line != 'suparati\n':
            listNames = line.split(' ')
            listNames[len(listNames) - 1] = listNames[len(listNames) - 1].rstrip()
            listAngry.append([listNames[0], listNames[1]])
        if task == 2:
            listNames = line.split(' ')
            listNames[len(listNames) - 1] = listNames[len(listNames) - 1].rstrip()
            startInput = listNames[1]
            finalInput = listNames[3]

    # print(matrInput)
    # print(listAngry)
    # print(startInput)
    # print(finalInput)

    rowStart = mapPosition[startInput][1]
    rowFinal = mapPosition[finalInput][1]
    colStart = mapPosition[startInput][0] * 2 + mapPosition[startInput][2]
    colFinal = mapPosition[finalInput][0] * 2 + mapPosition[finalInput][2]

    fileOutput = open('output.txt', 'w')
    fileOutput.seek(0)
    fileOutput.truncate()

    if startInput == finalInput:
        print(startInput)
        fileOutput.write(startInput)
    else:
        listFinal = solve(matrInput, listAngry, startInput, finalInput, whichEstimation, mapPosition)

        # AFISARE TRASEU
        out = ""
        if len(listFinal) != 0:
            out = out + listFinal[0].node.name
            print(listFinal[0].node.name, end=" ")
            for i in range(len(listFinal) - 1):
                first = listFinal[i]
                second = listFinal[i + 1]
                sign = verif_sign(first.node.name, second.node.name)
                out = out + " " + sign + " " + second.node.name
                print(" " + sign + " " + " " + second.node.name, end=" ")
        else:
            print("NU EXISTA SOLUTIE")
            out = "NU EXISTA SOLUTIE"
        fileOutput.write(out)

    t1 = time.time()
    print("")
    print("EXECUTION TIME: " + str(1000 * (t1 - t0) / 2) + " ms")
    fileOutput.write("\nEXECUTION TIME: " + str(1000 * (t1 - t0) / 2) + " ms")
    fileOutput.close()
    file.close()