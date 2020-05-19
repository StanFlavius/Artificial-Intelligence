import  time

class Node:
    def __init__(self, name, h, Neighbours):
        self.name = name
        self.h = h
        self.neighbours = []
        for i in Neighbours:
            self.neighbours.append(i)

class NodeParc:
    def __init__(self, name, parent, cost, f):
        self.name = name
        self.parent = parent
        self.cost = cost
        self.f = f

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

def solve(startInput, finalInput, nodesInput):
    nodes = nodesInput

    start = startInput
    final = finalInput

    firstNode = nodes[start]
    nodesParc = []
    firstNodeParc = NodeParc(firstNode.name, None, 0, 0)
    nodesParc.append(firstNodeParc)

    open = []
    closed = []
    open.append(nodesParc[0])
    while(len(open) != 0):
        open.sort()
        nodeCurr = open[0]
        '''for nod in open:
            if(nod.name != 'a'):
                print(str(nod.name) + " " + str(nod.parent.name) + " " + str(nod.f) + " " + str(nod.cost))
        print(nodeCurr.name)
        print("nextOPEN")'''
        open.remove(nodeCurr)
        closed.append(nodeCurr)
        if nodeCurr.name == final:
            print("Distanta de la " + start + " la " +  final  + " este " + str(nodeCurr.cost))
            print("Drumul este: ")
            parentList = []
            parentList.append(nodeCurr)

            while nodeCurr is not None:
                #print(nodeCurr.parent.name)
                parentList.append(nodeCurr.parent)
                nodeCurr = nodeCurr.parent

            parentList.reverse()
            for node in parentList:
                if node != None:
                    print(node.name,end=" ")
            break
        nameNodeCurr = nodeCurr.name
        nodeToExpand = nodes[nameNodeCurr]
        newNeighboursList = nodeToExpand.neighbours
        for neighbour in newNeighboursList:
            thatNode = nodes[neighbour[0]]
            exist = 0
            copy = nodeCurr
            while copy.parent != None:
                if copy.parent.name == neighbour[0]:
                    exist = 1
                    break
                copy = copy.parent

            if exist == 0:
                newNodeParc = NodeParc(neighbour[0], nodeCurr, nodeCurr.cost + neighbour[1], nodeCurr.cost + neighbour[1] + thatNode.h)
                exist = 0
                for i in closed:
                    if i.name == newNodeParc.name:
                        exist = 1
                        if newNodeParc.f < i.f:
                            closed.remove(i)
                            open.append(newNodeParc)
                if exist == 0:
                    for i in open:
                        if i.name == newNodeParc.name:
                            exist = 1
                            if newNodeParc.f < i.f :
                                open.remove(i)
                                open.append(newNodeParc)
                if exist == 0:
                    open.append(newNodeParc)

if __name__ == "__main__":
    t0 = time.time()
    nodesInput = {'a': Node('a', 0, [['b', 3], ['c', 9], ['d', 7]]), 'b': Node('b', 10, [['f', 100], ['e', 4]]),
     'c': Node('c', 3, [['e', 10], ['g', 6]]), 'd': Node('d', 7, [['i', 4]]), 'e': Node('e', 8, [['c', 1], ['f', 8]]),
     'f': Node('f', 0, []), 'g': Node('g', 14, [['e', 7]]), 'i': Node('i', 3, [['j', 2], ['k', 1]]),
     'j': Node('j', 1, []),
     'k': Node('k', 2, [])
     }
    start = 'a'
    final = 'f'
    solve(start, final, nodesInput)
    t1 = time.time()
    print("")
    print("EXECUTION TIME: " + str(1000 * (t1 - t0) / 2) + " ms")