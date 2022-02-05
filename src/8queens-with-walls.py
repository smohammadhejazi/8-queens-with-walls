import copy

W = 'W'
S = '*'

solutions = []
# Test 1
# problem = [[S, S, S, S, S, S, S, S],
#            [S, S, S, S, S, S, S, S],
#            [S, S, S, S, S, S, S, S],
#            [S, S, S, S, S, S, S, S],
#            [S, S, S, S, S, S, S, S],
#            [S, S, S, S, S, S, S, S],
#            [S, S, S, S, S, S, S, S],
#            [S, S, S, S, S, S, S, S]]

# Test 2
# problem = [[S, S, S, S, S, S, S, S],
#            [W, W, W, W, W, W, W, S],
#            [S, S, S, S, S, S, W, S],
#            [S, S, S, S, S, S, W, S],
#            [S, S, S, S, S, S, W, S],
#            [S, S, S, S, S, S, W, S],
#            [S, S, S, S, S, S, W, S],
#            [S, S, S, S, S, S, W, S]]

# Test 3
problem = [[S, S, S, W, W, S, S, S],
           [S, S, S, W, W, S, S, S],
           [S, S, S, W, W, S, S, S],
           [W, W, W, W, W, W, W, W],
           [W, W, W, W, W, W, W, W],
           [S, S, S, W, W, S, S, S],
           [S, S, S, W, W, S, S, S],
           [S, S, S, W, W, S, S, S]]

# Test 4
# problem = [[S, S, S, S, S, S, S, S],
#            [S, S, S, S, S, S, S, S],
#            [S, S, S, S, S, S, S, S],
#            [W, S, S, W, S, S, S, S],
#            [S, S, S, S, S, S, S, S],
#            [S, S, S, S, S, S, S, S],
#            [S, S, W, S, S, S, S, S],
#            [S, S, S, S, S, S, S, S]]


def printSolutions():
    for solution in solutions:
        printBoard(solution)


def printBoard(assignment):
    board = [[S for i in range(0, 8)] for j in range(0, 8)]
    for key, value in assignment.items():
        board[value[0]][value[1]] = key
    for i in range(0, 8):
        for j in range(0, 8):
            if board[i][j] != W and board[i][j] != S:
                print(str(board[i][j]) + "  ", end='')
            else:
                print(problem[i][j] + "  ", end='')
        print()
    print('\n')


def setDomain(assignment):
    domain = {}
    freeSquares = []
    for i in range(0, 8):
        for j in range(0, 8):
            if problem[i][j] != W:
                freeSquares.append((i, j))
    for key in assignment:
        domain[key] = copy.deepcopy(freeSquares)

    return domain


def inconsistentDomain(assignment):
    removedDomain = []
    value = assignment[1]
    # Self
    removedDomain.append(assignment[1])

    # Up
    for i in range(1, value[0] + 1):
        if problem[value[0] - i][value[1]] == W:
            break
        removedDomain.append((value[0] - i, value[1]))

    # Down
    for i in range(1, 8 - value[0]):
        if problem[value[0] + i][value[1]] == W:
            break
        removedDomain.append((value[0] + i, value[1]))

    # Left
    for i in range(1, value[1] + 1):
        if problem[value[0]][value[1] - i] == W:
            break
        removedDomain.append((value[0], value[1] - i))

    # Right
    for i in range(1, 8 - value[1]):
        if problem[value[0]][value[1] + i] == W:
            break
        removedDomain.append((value[0], value[1] + i))

    # Up Left
    for i in range(1, min(value[0] + 1, value[1] + 1)):
        if problem[value[0] - i][value[1] - i] == W:
            break
        removedDomain.append((value[0] - i, value[1] - i))

    # Up Right
    for i in range(1, min(value[0] + 1, 8 - value[1])):
        if problem[value[0] - i][value[1] + i] == W:
            break
        removedDomain.append((value[0] - i, value[1] + i))

    # Down Left
    for i in range(1, min(8 - value[0], value[1] + 1)):
        if problem[value[0] + i][value[1] - i] == W:
            break
        removedDomain.append((value[0] + i, value[1] - i))

    # Down Right
    for i in range(1, min(8 - value[0], 8 - value[1])):
        if problem[value[0] + i][value[1] + i] == W:
            break
        removedDomain.append((value[0] + i, value[1] + i))

    return removedDomain


def selectUnassigned(assignment):
    for key, value in assignment.items():
        if value is None:
            return key


def forwardCheck(newAssignment, domain):
    newDomain = copy.deepcopy(domain)
    removedDomain = inconsistentDomain(newAssignment)
    newDomain[newAssignment[0]] = newAssignment[1]
    del domain[newAssignment[0]]
    for removedSquare in removedDomain:
        for key, value in domain.items():
            for square in value:
                if square == removedSquare:
                    newDomain[key].remove(removedSquare)
                    break
    return newDomain


def addSolution(assignment):
    for solution in solutions:
        if set(solution.values()) == set(assignment.values()):
            return False
    solutions.append(assignment)
    return True


def isComplete(assignment):
    for key, value in assignment.items():
        if value is None:
            return False
    return True


def isFailure(domain):
    for key, value in domain.items():
        if len(value) == 0:
            return True
    return False


def backtracking(assignment, domain):
    if isFailure(domain):
        return False
    elif isComplete(assignment):
        if addSolution(assignment):
            printBoard(assignment)
        return True

    unassigned = selectUnassigned(assignment)
    for square in domain[unassigned]:
        assignment[unassigned] = square
        newDomain = forwardCheck((unassigned, square), copy.deepcopy(domain))
        backtracking(copy.deepcopy(assignment), copy.deepcopy(newDomain))
        assignment[unassigned] = None


if __name__ == "__main__":
    assignment = dict.fromkeys(['1', '2', '3', '4', '5', '6', '7', '8'])
    domain = setDomain(assignment)
    backtracking(assignment, domain)
    # printSolutions()
    print("Number of solutions = " + str(len(solutions)))