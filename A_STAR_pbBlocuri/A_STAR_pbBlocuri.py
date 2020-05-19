import copy
import time

class Node:
    def __init__(self,info):
        self.info = info
        self.estimate = 0

    def calculate_estime(self,list):
        copyInfo = copy.deepcopy(self.info)
        for i in copyInfo:
            i.reverse()
        copyList = copy.deepcopy(list)
        for i in copyList:
            i.reverse()
        no_of_diff = 0
        for i in range(len(copyList)):
            if len(copyInfo) > 0:
                for j in range(len(copyInfo[i])):
                    if j >= len(copyList[i]):
                        if copyInfo[i][j] is not None:
                            no_of_diff = no_of_diff + 1
                    elif copyInfo[i][j] != copyList[i][j]:
                            no_of_diff = no_of_diff + 1
        return no_of_diff

    def expand(self,parent, final):
        list_succesori = []
        info = self.info
        for i in range(len(info)):
            if len(info[i]) > 0:
                currElem = info[i][0]
                for j in range(len(info)):
                    if i != j:
                        copyInfo = copy.deepcopy(info)
                        copyInfo[i].pop(0)
                        copyInfo[j].insert(0,currElem)
                        node = Node(copyInfo)
                        node.estimate = node.calculate_estime(final.info)
                        newNodeParc = NodeParc(node, parent, parent.cost + 1)
                        list_succesori.append(newNodeParc)
        return  list_succesori

class NodeParc:
    def __init__(self, node, parent, cost):
        self.node = node
        self.parent = parent
        self.cost = cost
        self.f = cost + node.estimate

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
    start = Node(startInput)
    final = Node(finalInput)
    start.estimate = start.calculate_estime(final.info)

    first = NodeParc(start, None, 0)
    currState = first

    open = []
    closed = []
    open.append(first)

    gasitSol = 0

    while(len(open) > 0):
        open.sort()
        nodeCurr = open[0]
        open.remove(nodeCurr)
        closed.append(nodeCurr)
        listNext = nodeCurr.node.expand(nodeCurr, final)
        if nodeCurr.node.info == final.info:

            print("COST = " + str(nodeCurr.cost))
            gasitSol = 1
            parentList = []
            parentList.append(nodeCurr)
            while nodeCurr.parent != None:
                #print(nodeCurr.node.info)
                parentList.append(nodeCurr.parent)
                nodeCurr = nodeCurr.parent
            parentList.reverse()
            for k in range(len(parentList)):
                matr = copy.deepcopy(parentList[k].node.info)
                mx = 0
                for i in matr:
                    mx = max(mx, len(i))
                for i in matr:
                    for j in range(0, mx - len(i) + 1):
                        i.insert(0,' ')
                for i in range(len(matr)):
                    for j in range(len(matr[i])):
                        print(matr[j][i], end=" ")
                    print("")
                if k != len(parentList) - 1:
                    print("NEXT STEP IS: ")
            break

        if gasitSol == 1:
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
    a
    b c
    d
    final
    c b

    a d
    '''

    file = open('input', 'r')
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
            if l[0] != '':
                start.append(l)
            else:
                start.append([])
        if task == 2 and line != 'final\n':
            l = line.split(' ')
            l[len(l) - 1] = l[len(l) - 1].rstrip()
            if l[0] != '':
                final.append(l)
            else:
                final.append([])
    '''print(start)
    print(final)'''

    solve(start, final)
    t1 = time.time()
    print("EXECUTION TIME: " + str(1000 * (t1 - t0) / 2) + " ms")