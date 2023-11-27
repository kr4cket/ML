import numpy as np

FILE = open("matrix.txt.", "r")
str1 = FILE.readline()
size = str1.split(' ')

M = int(size[0])
N = int(size[1])

MATRIX = np.zeros((M, N), dtype=np.int32)
for i in range(M):
    s = FILE.readline()
    if len(s) == 0:
        break
    s1 = s.split(' ')
    for j in range(0, N):
        MATRIX[i][j] = int(s1[j])

FILE.close()
print("Game matrix: \n", MATRIX)

SIMPLEX = np.zeros((M + 1, N + M + 1), dtype=np.float64)
base = np.zeros(M + 1, dtype=np.int32)
P = np.zeros((M), dtype=np.float64)
Q = np.zeros((N), dtype=np.float64)
base[0] = 0

for i in range(1, M + 1):
    base[i] = i + N
SIMPLEX[0, 0] = 0
for i in range(1, M + 1):
    SIMPLEX[i, 0] = 1
for i in range(1, N + 1):
    SIMPLEX[0, i] = -1
for i in range(1, M + 1):
    for j in range(1, N + 1):
        SIMPLEX[i, j] = MATRIX[i - 1, j - 1]
    for k in range(1, M + 1):
        SIMPLEX[k, N + k] = 1

print("Simplex table: \n")
for i in range(0, M + 1):
    print("%.d " % base[i], end="")
    for j in range(0, N + M + 1):
        print("%6.3f " % SIMPLEX[i][j], end="")
    print('')

counter = 0
while True:
    mainCol = SIMPLEX[0, 3]
    numOfMainCol = 3
    for i in range(2, M + N + 1):
        if (SIMPLEX[0, i] < mainCol):
            mainCol = SIMPLEX[0, i]
            numOfMainCol = i
    if (mainCol >= 0):
        break
    mainStr = 100000
    numOfMainStr = 0
    for i in range(1, M + 1):
        if (SIMPLEX[i, numOfMainCol] > 0):
            h = SIMPLEX[i, 0] / SIMPLEX[i, numOfMainCol]
            if (h < mainStr):
                mainStr = h
                numOfMainStr = i
    if (numOfMainStr == 0):
        print("No resolutions")
        break
    for i in range(0, M + 1):
        for j in range(0, M + N + 1):
            if i != numOfMainStr and j != numOfMainCol:
                SIMPLEX[i, j] = SIMPLEX[i, j] - SIMPLEX[numOfMainStr, j] * SIMPLEX[i, numOfMainCol] / SIMPLEX[
                    numOfMainStr, numOfMainCol]
    for j in range(0, M + N + 1):
        if (j != numOfMainCol):
            SIMPLEX[numOfMainStr, j] = SIMPLEX[numOfMainStr, j] / SIMPLEX[numOfMainStr, numOfMainCol]
    for i in range(0, M + 1):
        SIMPLEX[i, numOfMainCol] = 0
    SIMPLEX[numOfMainStr, numOfMainCol] = 1
    base[numOfMainStr] = numOfMainCol
    counter += 1
    print("Simplex table after iteration %.d: " % counter)
    for i in range(0, M + 1):
        print("%.d " % base[i], end="")
        for j in range(0, N + M + 1):
            print("%6.3f " % SIMPLEX[i][j], end="")
        print('')
priceOfGame = 1 / SIMPLEX[0, 0]
print("Game cost: %.3f " % (priceOfGame))
for i in range(0, M):
    P[i] = SIMPLEX[0, N + i + 1] * priceOfGame
print("Variativity for the first person: ")
for i in range(0, M):
    print("P[" + str(i + 1) + "] = " + "%.3f " % P[i])
for j in range(0, M + 1):
    z = base[j]
    if (z >= 0 and z <= N):
        q = SIMPLEX[j, 0]
        Q[z - 1] = q * priceOfGame
print("Variativity for the second person: ")
for i in range(0, N):
    print("Q[" + str(i + 1) + "] = " + "%.3f " % Q[i])
