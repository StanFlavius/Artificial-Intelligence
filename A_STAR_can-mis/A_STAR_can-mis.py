import copy
import time

class Node:
    def __init__(self, info):
        self.info = info
        self.h = 0

    def calculate_estimation(self, N, M):
        if self.info[0] == 0:
            estimation = 2 * ( self.info[1] + self.info[2]) // M - 1
        else:
            estimation = 2 * ( N - self.info[1] + N - self.info[2]) // M
        return estimation

    def expand(self, N, M, parent):
        listSucc = []
        nrMisCurr = self.info[1]
        nrCanibCurr = self.info[2]
        nrMisOp = N - nrMisCurr
        nrCanibOp = N - nrCanibCurr

        #trimit doar canibali
        for nrCanibTrv in range(1, min(M, nrCanibCurr) + 1):
            if nrMisOp >= nrCanibOp + nrCanibTrv or nrMisOp == 0:
                newMis = nrMisOp
                newCanib = nrCanibOp + nrCanibTrv
                newNode = Node((1-self.info[0], newMis, newCanib))
                newNode.h = newNode.calculate_estimation(N, M)
                newNodeParc = NodeParc(newNode, parent, parent.cost + 1)
                listSucc.append(newNodeParc)

        #trimit doar misionari
        for nrMisTrv in range(1, min(M, nrMisCurr) + 1):
            if nrMisOp + nrMisTrv >= nrCanibOp and ( nrMisCurr - nrMisTrv >= nrCanibCurr or nrMisCurr - nrMisTrv == 0):
                newMis = nrMisOp + nrMisTrv
                newCanib = nrCanibOp
                newNode = Node((1-self.info[0], newMis, newCanib))
                newNode.h = newNode.calculate_estimation(N, M)
                newNodeParc = NodeParc(newNode, parent, parent.cost + 1)
                listSucc.append(newNodeParc)

        #trimit si misionari si canibali
        for nrMisTrv in range(1, min(M, nrMisCurr) + 1):
            for nrCanibTrv in range(1, min(M - nrMisTrv, nrMisTrv) + 1):
                if nrMisOp + nrMisTrv >= nrCanibOp + nrCanibTrv and nrMisCurr - nrMisTrv >= nrCanibCurr - nrCanibTrv:
                    newMis = nrMisOp + nrMisTrv
                    newCanib = nrCanibOp + nrCanibTrv
                    newNode = Node((1 - self.info[0], newMis, newCanib))
                    newNode.h = newNode.calculate_estimation(N, M)
                    newNodeParc = NodeParc(newNode, parent, parent.cost + 1)
                    listSucc.append(newNodeParc)

        return listSucc

class NodeParc:
    def __init__(self, node, parent, cost):
        self.node = node
        self.parent = parent
        self.cost = cost
        self.f = cost + node.h

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

def solve(N, M):

    start = (0, N, N)
    final = (1, N, N)

    nodeStart = Node(start)
    nodeStart.h = nodeStart.calculate_estimation(N, M)

    nodeParcStart = NodeParc(nodeStart, None, 0)

    open = []
    open.append(nodeParcStart)
    closed = []

    ok = 0

    while len(open) > 0:
        open.sort()
        nodeCurr = open[0]
        open.remove(nodeCurr)
        closed.append(nodeCurr)

        listSucc = nodeCurr.node.expand(N, M, nodeCurr)

        if nodeCurr.node.info == final:
            ok = 1
            print("SOLVABLE")
            print("WE NEED " + str(nodeCurr.cost) + " CROSSINGS")
            parentList = []
            parentList.append(nodeCurr)
            while nodeCurr.parent is not None:
                parentList.append(nodeCurr.parent)
                nodeCurr = nodeCurr.parent
            parentList.reverse()
            for i in parentList:
                if i.node.info[0] == 0:
                    print("LEFT SIDE: " + str(i.node.info[1]) + " MISSIONERS AND " + str(i.node.info[2]) + " CANIBALS"
                        + " ---- RIGHT SIDE:  " + str(N - i.node.info[1]) + " MISSIONERS AND " + str(N - i.node.info[2]) + " CANIBALS")
                else:
                    print("LEFT SIDE: "+ str(N - i.node.info[1]) + " MISSIONERS AND " + str(N - i.node.info[2]) + " CANIBALS"
                          + " ---- RIGHT SIDE:  " + str(i.node.info[1]) + " MISSIONERS AND " + str(i.node.info[2]) + " CANIBALS")

        for k in range(len(listSucc)):
            newNodeParc = listSucc[k]
            copyNode = nodeCurr
            exist = 0
            while copyNode.parent is not None:
                if copyNode.parent == newNodeParc:
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

    if ok == 0:
        print("UNSOLVABLE")

if __name__ == "__main__":
    t0 = time.time()

    #MODEL INPUT
    '''
    3
    2
    '''

    file = open('input','r')
    l = []
    for line in file:
        line = line.rstrip()
        l.append(line)

    N = int(l[0])
    M = int(l[1])

    solve(N, M,)
    t1 = time.time()
    print("")
    print("EXECUTION TIME: " + str(1000 * (t1 - t0) / 2) + " ms")