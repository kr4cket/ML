import numpy as np

f = open('matrix.txt', 'r')
s = f.readline()
s1 = s.split(' ')
M = int(s1[0])
N = int(s1[1])
MATRIX = np.zeros((M, N), dtype=np.int32)
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
K = 5  # в зависимости от количества итераций
Z = M + N + 5
it = np.zeros((K, Z), dtype=np.int32)
P = np.zeros((M), dtype=np.float64)
Q = np.zeros((N), dtype=np.float64)
for i in range(0, M):
    P[i] = 0
for i in range(0, N):
    Q[i] = 0
it[0, 0] = 1
it[0, 1] = 2
P[1] = 1
for k in range(0, K):
    it[k, 0] = k + 1
    for i in range(0, N):
        d = it[k, 1] - 1
        it[k, i + 2] = it[k - 1, i + 2] + MATRIX[d, i]
    Min = it[k, 2]
    Nmin = 0
    for i in range(0, N):
        if (it[k, i + 2] < Min):
            Min = it[k, i + 2]
            Nmin = i
    it[k, N + 2] = Min
    it[k, N + 3] = Nmin + 1
    Vmin = Min
    t = Nmin
    Q[t] += 1
    for i in range(0, M):
        it[k, N + 4 + i] = it[k - 1, N + 4 + i] + MATRIX[i, t]
    Nmax = 0
    Max = it[k, N + 4]
    for i in range(0, M):
        if (it[k, N + 4 + i] > Max):
            Max = it[k, N + 4 + i]
            Nmax = i
    it[k, N + M + 4] = Max
    if (k < K - 1):
        it[k + 1, 1] = Nmax + 1
    Vmax = Max
    if (k < K - 1):
        P[Nmax] += 1
print("Iteration table after " + str(K) + " iteration:")
for i in range(0, Z):
    print("%.d " % it[K - 1][i], end=" ")
for i in range(0, M):
    P[i] = P[i] / K
for i in range(0, N):
    Q[i] = Q[i] / K
gamecost = (Vmax + Vmin) / (2 * K)
print("\n Game cost:")
print("%.3f" % gamecost)
print("Variativity for the first person: ")
for i in range(0, M):
    print("P[" + str(i + 1) + "] = " + "%.3f " % P[i])
print("Variativity for the second person: ")
for i in range(0, N):
    print("Q[" + str(i + 1) + "] = " + "%.3f " % Q[i])
