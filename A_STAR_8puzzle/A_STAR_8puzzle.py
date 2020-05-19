import copy
import time

class node:
    def __init__(self,info):
        self.info = info
        self.estimation = 0

    def verif_input(self):
        list = []
        for i in self.info:
            for j in i:
                if j != '0':
                    list.append(j)
        no_of_inv = 0
        for i in range(len(list)):
            for j in range(i,len(list)):
                if int(list[i]) > int(list[j]):
                    no_of_inv = no_of_inv + 1
        #print(no_of_inv)
        if no_of_inv % 2 == 1:
            return False
        return True

    def calculate_estimation(self, configFin):
        no_of_diff = 0
        for i in range(len(self.info)):
            for j in range(len(self.info)):
                if self.info[i][j] != configFin.info[i][j]:
                    no_of_diff = no_of_diff + 1
        return no_of_diff

    def expand(self, parent, final):
        listSuccesors = []
        pozI = -1
        pozJ = -1
        for i in range(len(self.info)):
            for j in range(len(self.info)):
                if self.info[i][j] == '0':
                    pozI = i
                    pozJ = j

        if pozI - 1 > -1:
            copyInfo = copy.deepcopy(self.info)
            val = copyInfo[pozI - 1][pozJ]
            copyInfo[pozI - 1][pozJ] = '0'
            copyInfo[pozI][pozJ] = val
            newNode = node(copyInfo)
            newNode.estimation = newNode.calculate_estimation(final)
            newNodeParc = nodeParc(newNode, parent, parent.cost + 1)
            listSuccesors.append(newNodeParc)

        if pozI + 1 < len(self.info):
            copyInfo = copy.deepcopy(self.info)
            val = copyInfo[pozI + 1][pozJ]
            copyInfo[pozI + 1][pozJ] = '0'
            copyInfo[pozI][pozJ] = val
            newNode = node(copyInfo)
            newNode.estimation = newNode.calculate_estimation(final)
            newNodeParc = nodeParc(newNode, parent, parent.cost + 1)
            listSuccesors.append(newNodeParc)

        if pozJ - 1 > -1:
            copyInfo = copy.deepcopy(self.info)
            val = copyInfo[pozI][pozJ - 1]
            copyInfo[pozI][pozJ - 1] = '0'
            copyInfo[pozI][pozJ] = val
            newNode = node(copyInfo)
            newNode.estimation = newNode.calculate_estimation(final)
            newNodeParc = nodeParc(newNode, parent, parent.cost + 1)
            listSuccesors.append(newNodeParc)

        if pozJ + 1 < len(self.info):
            copyInfo = copy.deepcopy(self.info)
            val = copyInfo[pozI][pozJ + 1]
            copyInfo[pozI][pozJ + 1] = '0'
            copyInfo[pozI][pozJ] = val
            newNode = node(copyInfo)
            newNode.estimation = newNode.calculate_estimation(final)
            newNodeParc = nodeParc(newNode, parent, parent.cost + 1)
            listSuccesors.append(newNodeParc)

        return listSuccesors

class nodeParc:
    def __init__(self,node, parent, cost):
        self.node = node
        self.parent = parent
        self.cost = cost
        self.f = cost + node.estimation

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

def solve(startInput, finalInput):
    final = node(finalInput)
    start = node(startInput)

    start = nodeParc(start, None, 0)

    if start.node.verif_input() == False:
        print("UNSOLVABLE")
        return

    print("SOLVABLE")

    open = []
    closed = []
    open.append(start)

    while len(open) > 0:
        #print(len(open))
        open.sort()
        nodeCurr = open[0]

        open.remove(nodeCurr)
        closed.append(nodeCurr)
        listNext = nodeCurr.node.expand(nodeCurr, final)

        ok = 0

        #print(nodeCurr.node.info)
        if nodeCurr.node.info == final.info:
            ok = 1
            print("WE NEED " + str(nodeCurr.cost) + " MOVES")
            parentList = []
            parentList.append(nodeCurr)
            while nodeCurr.parent != None:
                while nodeCurr.parent != None:
                    # print(nodeCurr.node.info)
                    parentList.append(nodeCurr.parent)
                    nodeCurr = nodeCurr.parent
            parentList.reverse()
            for k in range(len(parentList)):
                matr = copy.deepcopy(parentList[k].node.info)
                for i in matr:
                    for j in i:
                        print(j,end=" ")
                    print("")
                if k != len(parentList) - 1:
                    print("NEXT MATRIX IS : ")
                #print(nodeP.node.info, end="\n")

        if ok == 1:
            break

        for k in range(len(listNext)):
            newNodeParc = listNext[k]
            exist = 0
            copyNode = nodeCurr
            while copyNode.parent is not None:
                if copyNode.parent.node.info == newNodeParc.node.info:
                    exist = 1
                    break
                copyNode = copyNode.parent

            if exist == 0:
                exist = 0
                for i in closed:
                    if i.node.info == newNodeParc.node.info:
                        exist = 1
                        if newNodeParc.f < i.f:
                            closed.remove(i)
                            open.append(newNodeParc)
                if exist == 0:
                    for i in open:
                        if newNodeParc.node.info == i.node.info:
                            exist = 1
                            if newNodeParc.f < i.f:
                                open.remove(i)
                                open.append(newNodeParc)
                if exist == 0:
                    open.append(newNodeParc)

if __name__ == "__main__":
    t0 = time.time()

    #MODEL INPUT
    '''
    start
    0 7 6
    5 8 1
    2 4 3
    final
    1 2 3
    4 5 6
    7 8 0
    '''

    file = open('input','r')
    start = []
    final = []
    task = 0
    for line in file:
        if line == 'start\n':
            task = 1
        if line == 'final\n':
            task = 2
        if task == 1 and line != 'start\n':
            l = line.split(' ')
            l[len(l) - 1] = l[len(l) - 1].rstrip()
            start.append(l)
        if task == 2 and line != 'final\n':
            l = line.split(' ')
            l[len(l) - 1] = l[len(l) - 1].rstrip()
            final.append(l)

    solve(start, final)
    t1 = time.time()
    print("EXECUTION TIME: " + str(1000 * (t1 - t0) / 2) + " ms")