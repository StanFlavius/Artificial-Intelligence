class clasa:
    def __init__(self, val1, val2):
        self.val1 = val1
        self.val2 = val2

    def __lt__(self, other):
        if other.val1 == self.val1:
            if other.val2 > self.val2:
                return 0
            else:
                return 1
        elif other.val1 < self.val1:
            return 0
        else:
            return 1


vec = []
cls1 = clasa(5, 1)
cls2 = clasa(3, 1)
cls3 = clasa(5, 2)

vec.append(cls1)
vec.append(cls2)
vec.append(cls3)

for i in vec:
    print(str(i.val1) + " " + str(i.val2))

print("\n")
vec.sort()

for i in vec:
    print(str(i.val1) + " " + str(i.val2))
