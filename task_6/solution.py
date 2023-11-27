from scipy.optimize import linprog
import numpy as np

f = open('matrix.txt', 'r')
s = f.readline()
s1 = s.split(' ')
M = int(s1[0])
N = int(s1[1])
MATRIX = np.zeros((M, N), dtype=np.int32)
P = np.zeros((M), dtype=np.float64)
Q = np.zeros((N), dtype=np.float64)
A = np.zeros((N, M), dtype=np.int32)
for i in range(0, M):
    s = f.readline()
    if len(s) == 0:
        break
    s1 = s.split(' ')
    for j in range(0, N):
        MATRIX[i][j] = int(s1[j])
f.close()
print("Game matrix:")
print(MATRIX)
b = []
c = []
for i in range(0, M):
    c.append(1)
for i in range(0, N):
    b.append(-1)
for i in range(0, N):
    for j in range(0, M):
        A[i][j] = -MATRIX[j][i]
x0_bnds = (0, None)
x1_bnds = (0, None)
x2_bnds = (0, None)
res = linprog(c, A, b, bounds=(x0_bnds, x1_bnds, x2_bnds))
gamecost = res.fun
gamecost = 1 / gamecost
print("Game cost for the first person: %.3f " % (gamecost))
for i in range(0, M):
    P[i] = res.x[i] * gamecost
print("Variativity fo the first person: ")
for i in range(0, M):
    print("P[" + str(i + 1) + "] = " + "%.3f " % P[i])
b = []
c = []
for i in range(0, N):
    c.append(-1)
for i in range(0, M):
    b.append(1)
A = np.zeros((M, N), dtype=np.int32)
for i in range(0, M):
    for j in range(0, N):
        A[i][j] = MATRIX[i][j]
x0_bnds = (0, None)
x1_bnds = (0, None)
x2_bnds = (0, None)
x3_bnds = (0, None)
res = linprog(c, A, b, bounds=(x0_bnds, x1_bnds, x2_bnds, x3_bnds))
gamecost = res.fun
gamecost = 1 / gamecost
gamecost = -gamecost
print("Variativity for the second person: %.3f " % (gamecost))
for i in range(0, N):
    Q[i] = res.x[i] * gamecost
print("Game cost for the second person: ")
for i in range(0, N):
    print("Q[" + str(i + 1) + "] = " + "%.3f " % Q[i])
