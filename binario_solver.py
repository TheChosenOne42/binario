
field = []
moves = []
assumptions = []
debug_level = 0

def solvePairs(findwhat, placewhat):
    if debug_level > 0:
        print("solvePairs", findwhat, placewhat)
        printField()
    for y in range(1, N+1):
        for x in range(1, N+1):
            if field[y][x-1] + field[y][x] + field[y][x+1] == findwhat + " " + findwhat:
                checkAndMove(x, y, placewhat)
            if field[y][x-1] == field[y][x] and field[y][x] == findwhat:
                checkAndMove(x+1, y, placewhat)
                checkAndMove(x-2, y, placewhat)
            if field[y-1][x] + field[y][x] + field[y+1][x] == findwhat + " " + findwhat:
                checkAndMove(x, y, placewhat)
            if field[y-1][x] == field[y][x] and field[y][x] == findwhat:
                checkAndMove(x, y+1, placewhat)
                checkAndMove(x, y-2, placewhat)
    if debug_level > 0:
        print("solvePairs end", findwhat, placewhat)
        printField()

def checkAndMove(x, y, placewhat):
    if x>0 and y>0 and field[y][x] == " ":
        field[y][x] = placewhat
        moves.append((x, y, placewhat))
        return True
    return False

def uniqueRow(y):
    currentLine = field[y][1:]
    found = False
    for a in currentLine:
        if a == " ":
            found = True
            break
    if not found:
        for y1 in range(1, N+1):
            if y1 == y:
                continue
            if field[y1][1:] == currentLine:
                return False
    return True

def uniqueCol(x):
    currentCol = []
    for y0 in range(1, N+1):
        currentCol.append(field[y0][x])
    #print(currentCol)
    found = False
    for a in currentCol:
        if a == " ":
            found = True
            break
    if not found:
        for x1 in range(1, N+1):
            if x1 == x:
                continue
            #if field[x1][1:] == currentCol:
            currentCol3=[]
            for y0 in range(1, N+1):
                currentCol3.append(field[y0][x1])   
            if currentCol3 == currentCol:
                return False
    return True

def assumeMove(x, y, placewhat):
    # 1. Each row and each column must contain an equal number of white and black circles.
    #   already taken care of by finishLine() call right before this one 
    # 2. More than two circles of the same color can't be adjacent.
    #   dont do because of solvePairs() call right before in automaticSolving(). 
    # 3. Each row and column is unique.
    if not uniqueRow(y):
        return False
    if not uniqueCol(x):
        return False
    if not checkAndMove(x, y, placewhat):
        return False
    #moves.append((x, y, placewhat))
    assumptions.append(len(moves)-1)
    if debug_level > 0:
        print("new assumption ", x, y, placewhat)
    return True
    
def printField():
    for line in field:
        print(''.join(line))

def findSpace():
    for y in range(1, N+1):
        for x in range(1, N+1):
            if field[y][x] == " ":
                return (x, y, True)
    return (0, 0, False)

def finishLine(findwhat, placewhat):
    if debug_level > 0:
        print("finishLine")
        printField()
    for y in range(1, N+1):
        count = 0
        for x in range(1, N+1):
            if field[y][x] == findwhat:
                count += 1
        if count == N/2:
            for x in range(1, N+1):
                if checkAndMove(x, y, placewhat):
                    if x>2 and field[y][x-2] == placewhat and field[y][x-1] == placewhat:
                        #print("finishLine row", x, y, findwhat, placewhat)
                        return False
    for x in range(1, N+1):
        count = 0
        for y in range(1, N+1):
            if field[y][x] == findwhat:
                count += 1
        if count == N/2:
            for y in range(1, N+1):
                if checkAndMove(x, y, placewhat):
                    if y>2 and field[y-2][x] == placewhat and field[y-1][x] == placewhat:
                        #print("finishLine col", x, y, findwhat, placewhat)
                        return False
    return True

def changeAssumption():
    if debug_level > 0:
        print("changeAssumption")
        printField()
    while True:
        if debug_level > 0:
            print(assumptions)
        lastAssumptionIndex = assumptions.pop()
        lastAssumption = moves[lastAssumptionIndex]
        (x, y, what) = lastAssumption
        if debug_level > 0:
            print("change assumption ", x, y, what)
        for a in range(lastAssumptionIndex, len(moves)):
            (x, y, p) = moves.pop()
            #print(x, y)
            field[y][x] = " "
        if what == "O":
            # we could try X assumptions
            if assumeMove(x, y, "X"):
                return
            continue
        continue  

def automaticSolving():
    while True:
        if debug_level > 0:
            print("automaticSolving")
            printField()
        l = len(moves)
        solvePairs("X", "O")
        solvePairs("O", "X")
        if not finishLine("X", "O"):
            changeAssumption()
            continue
        if not finishLine("O", "X"):
            changeAssumption()
            continue
        if l == len(moves):
            break
    if debug_level > 0:
        print("automtic solving end")
        printField()
    
def checkValidity():
    # 1. Each row and each column must contain an equal number of white and black circles.
    for what in ["X", "O"]:
        for y in range(1, N+1):
            count = 0
            for x in range(1, N+1):
                if field[y][x] == what:
                    count += 1
                    if count > N/2:
                        return str(x)+" "+str(y)+" "+what+" too many in a row"
        for x in range(1, N+1):
            count = 0
            for y in range(1, N+1):
                if field[y][x] == what:
                    count += 1
                    if count > N/2:
                        return str(x)+" "+str(y)+" "+what+" too many in a col"
    # 2. More t han two circles of the same color can't be adjacent.
    for y in range(1, N+1):
        for x in range(1, N+1):
            for placewhat in ["X", "O"]:
                '''if field[y-1][x] == placewhat:
                        if y>2 and field[y-2][x] == placewhat:
                            return str(x)+" "+str(y)+" "+placewhat+" mistery 1"
                        if field[y+1][x] == placewhat:
                            return str(x)+" "+str(y)+" "+placewhat+" mistery 2"
                    if field[y][x-1] == placewhat:
                        if x>2 and field[y][x-2] == placewhat:
                            return str(x)+" "+str(y)+" "+placewhat+" mistery 3"
                        if field[y][x+1] == placewhat:
                            return str(x)+" "+str(y)+" "+placewhat+" mistery 4"
                    if field[y+1][x] == placewhat:
                        if y+2<N+1 and field[y+2][x] == placewhat:
                            return str(x)+" "+str(y)+" "+placewhat+" mistery 5"
                    if field[y][x+1] == placewhat:
                        if x+2<N+1 and field[y][x+2] == placewhat:
                            return str(x)+" "+str(y)+" "+placewhat+" mistery 6"'''
                '''if field[4][2] == field[4][3] and field[4][3] == field[4][4]:
                    return False'''
                if field[y][x] == placewhat and field[y-1][x] == placewhat and field[y+1][x] == placewhat:
                    return str(x)+" "+str(y)+" "+placewhat+" three in a col"
                if field[y][x] == placewhat and field[y][x-1] == placewhat and field[y][x+1] == placewhat:
                    return str(x)+" "+str(y)+" "+placewhat+" three in a row"
    # 3. Each row and column is unique.
    for y in range(1, N+1):
        x = y
        if not uniqueRow(y):
            return str(x)+" "+str(y)+" not unique row"
        if not uniqueCol(x):
            return str(x)+" "+str(y)+" not unique col"
    return ""
    
#for fname in ["input1.txt", "input2.txt", "input3.txt", "input4.txt", "input5.txt", "input6.txt"]:
for fname in ["input12.txt"]:
    f = open(fname, "r")
    field = []
    for line0 in f:
        line = list(line0.rstrip())
        field.append(line)
    f.close()
    N = len(field) - 2
    moves = []
    assumptions = []
    #printField(field)
    while True:
        automaticSolving()
        res = checkValidity()
        if not res == "":
            print("checkValidity failed: ", res)
            changeAssumption()
            continue
        (x, y, found) = findSpace()
        if not found:
            break
        if assumeMove(x, y, "O"):
            pass
        elif assumeMove(x, y, "X"):
            pass
        else:
            # TODO: keep looking for valid assumption somewhere else
            pass
        if debug_level > 0:
            print("main loop")
            printField()
    print("main", fname)
    printField()
    print(moves)
    print(assumptions)
    for a in assumptions:
        print(moves[a])
    
    
