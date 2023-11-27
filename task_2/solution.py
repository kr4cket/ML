from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import numpy as np

Obr = 30
Siz = 36
TestObr = 9
ClustCntr = np.zeros((Obr, Siz), dtype=np.float64)
ClustersROW = np.zeros((Obr), dtype=np.int32)
ClustersOldROW = np.zeros((Obr), dtype=np.int32)
NumOfClusters = np.zeros((Obr), dtype=np.int32)
FILE = open('FILE2.txt', 'r')
LETTERS = np.zeros((Obr, Siz), dtype=np.int32)
num = 0

while True:
    s = FILE.readline()
    if len(s) == 0:
        break
    s = s.split(" ")
    for i in range(Siz):
        LETTERS[num, i] = int(s[i])
    num += 1
FILE.close()


def EvklidLength(p, q, Arr):
    y = 0
    for j in range(Siz):
        y += (ClustCntr[p, j] - Arr[q, j]) * (ClustCntr[p, j] - Arr[q, j])
    return y


def EvklidCenterLength(p, q):
    y = 0
    for j in range(Siz):
        y += (ClustCntr[p, j] - ClustCntr[q, j]) * (ClustCntr[p, j] - ClustCntr[q, j])
    return y


def DistributeObr(Arr):
    for i in range(Obr):
        MinValue = 3000
        Nk = 0
        for k in range(K):
            z = EvklidLength(k, i, Arr)
            if (z < MinValue):
                Nk = k
                MinValue = z
        ClustersROW[i] = Nk


def DistributeObrMinMax(Arr):
    global Nvect
    global D
    Nvect = 0
    D = 0
    for i in range(Obr):
        MinVal = 30000
        NK = 0
        for k in range(K):
            z = EvklidLength(k, i, Arr)
            if (z < MinVal):
                NK = k
                MinVal = z
        ClustersROW[i] = NK
        if (MinVal > D):
            Nvect = i
            D = MinVal


def CalcDist():
    global Dmean
    Dmean = 0
    for i in range(K):
        for j in range(i, K):
            Z = EvklidCenterLength(i, j)
            Dist[i, j] = Z
            Dmean += Z
    Dmean = (int)(Dmean / K)


def ComputenNewCenter(Arr):
    for k in range(K):
        NumOfClusters[k] = 0
        for j in range(Siz):
            ClustCntr[k, j] = 0

    for i in range(Obr):
        m = ClustersROW[i]
        for j in range(Siz):
            ClustCntr[m, j] = ClustCntr[m, j] + Arr[i, j]
        NumOfClusters[m] = NumOfClusters[m] + 1

    for h in range(K):
        for g in range(Siz):
            ClustCntr[h, g] = ClustCntr[h, g] / NumOfClusters[h]


choose = int(input("Choose 0 or 1: "))

if choose == 0:
    K = 3
    LetterCenter = np.zeros((Obr), dtype=np.int32)
    LetterCenter[0] = 0
    LetterCenter[1] = 1
    LetterCenter[2] = 7
    for i in range(K):
        M = LetterCenter[i]
        for j in range(Siz):
            ClustCntr[i, j] = LETTERS[M, j]
    DistributeObr(LETTERS)
    F = True
    while F:
        for i in range(Obr):
            ClustersOldROW[i] = ClustersROW[i]
        ComputenNewCenter(LETTERS)
        DistributeObr(LETTERS)
        F = False
        print(ClustersOldROW)
        for i in range(Obr):
            if ClustersOldROW[i] != ClustersROW[i]:
                F = True
else:
    K = 1
    Dist = np.zeros((Obr, Obr), dtype=np.int32)
    for i in range(Siz):
        ClustCntr[0, i] = LETTERS[0, i]
    F = True
    while F:
        DistributeObrMinMax(LETTERS)
        CalcDist()
        if D < Dmean:
            break
        for j in range(Siz):
            ClustCntr[K, j] = LETTERS[Nvect, j]
        K += 1
        print(ClustersROW)
    DistributeObrMinMax(LETTERS)
    print(ClustersROW)

IMG = Image.new('RGB', (1200, 1200), (155, 155, 155))
DRAW = ImageDraw.Draw(IMG)
FNT = ImageFont.truetype('arial.ttf', 45)


def DrawOneEl(x, y, El, xn, L, Array):
    for i in range(Siz):
        if Array[El, i] == 1:
            DRAW.rectangle(((x, y), (x + L, y + L)), fill="black", outline="black")
        else:
            DRAW.rectangle(((x, y), (x + L, y + L)), fill="white", outline="white")
        x += L
        if (i + 1) % 6 == 0 and i != 0:
            x = xn
            y += L
        if i == 35:
            DRAW.text((x + 40, y), str(ClustersROW[El]), fill=(0, 0, 255), font=FNT)


def DrawOneHalfTone(x, y, OldSize, NewSize, xn, L, Arrs):
    for i in range(OldSize, NewSize):
        DRAW.rectangle(((x, y), (x + L, y + L)), fill=(Arrs[i], Arrs[i], Arrs[i]), outline="black")
        x += L
        if (i + 1) % 6 == 0 and i != 0:
            x = xn
            y += L


def DrawRowofEl(x, y, xn, OldEL, El, L, Array):
    for i in range(OldEL, El):
        DrawOneEl(x, y, i, xn, L, Array)
        xn += 6 * L + 10
        x = xn


def DrawRowofHalfTone(x, y, xn, K, L, Arrs):
    OldSize = 0
    NewSize = 36
    for i in range(K):
        DrawOneHalfTone(x, y, OldSize, NewSize, xn, L, Arrs)
        xn += 6 * L + 10
        OldSize = NewSize
        NewSize += 36
        x = xn


def DrawAllLetters(Rows, ElRow, x, y, xn, L, Array):
    OldRow = 0
    for i in range(Rows):
        DrawRowofEl(x, y, xn, OldRow, ElRow, L, Array)
        xn = 0
        x = xn
        y += 150
        OldRow = ElRow
        ElRow += 10


DrawAllLetters(3, 10, 0, 0, 0, 15, LETTERS)

Arrs = []
Classes = np.zeros((K), dtype=np.int32)
ClassesArr = np.zeros((Obr, Siz), dtype=np.int32)


def makingCountClasses():
    temp = 0
    for i in range(K):
        Classes[i] = 0

    for i in range(K):
        for j in range(Obr):
            if i == ClustersROW[j]:
                Classes[i] += 1
                Arrs.append(LETTERS[j])
                ClassesArr[temp] = LETTERS[j]
                temp += 1


def makeClasses():
    makingCountClasses()
    OLD = 0
    i = 0
    s = 0
    Arrs = []
    for j in range(Obr):
        for k in range(Siz):
            for g in range(Classes[i]):
                if ClassesArr[g + OLD, k] == 1:
                    s += 1
            s = 256 - int((s * 160) / Classes[i])
            if s == 256:
                s -= 1
            Arrs.append(s)
            s = 0

        OLD = Classes[i]
        i += 1
        if i == K:
            break
    return Arrs


DrawRowofHalfTone(0, 500, 0, K, 15, makeClasses())

FILE = open('TEST.txt', 'r')

Obr = 9
TEST = np.zeros((Obr, Siz), dtype=np.int32)
num = 0
while True:
    s = FILE.readline()
    if len(s) == 0:
        break
    s = s.split(" ")
    for i in range(Siz):
        TEST[num, i] = int(s[i])
    num += 1
FILE.close()

ClustCntr = np.zeros((Obr, Siz), dtype=np.float64)
ClustersROW = np.zeros((Obr), dtype=np.int32)
ClustersOldROW = np.zeros((Obr), dtype=np.int32)
NumOfClusters = np.zeros((Obr), dtype=np.int32)

if choose == 0:
    K = 3
    LetterCenter = np.zeros((Obr), dtype=np.int32)
    LetterCenter[0] = 2
    LetterCenter[1] = 1
    LetterCenter[2] = 0
    for i in range(K):
        M = LetterCenter[i]
        for j in range(Siz):
            ClustCntr[i, j] = TEST[M, j]
    DistributeObr(TEST)
    F = True
    while F:
        for i in range(Obr):
            ClustersOldROW[i] = ClustersROW[i]
        ComputenNewCenter(TEST)
        DistributeObr(TEST)
        F = False
        print(ClustersOldROW)
        for i in range(Obr):
            if ClustersOldROW[i] != ClustersROW[i]:
                F = True
else:
    K = 1
    Dist = np.zeros((Obr, Obr), dtype=np.int32)
    for i in range(Siz):
        ClustCntr[0, i] = TEST[0, i]
    F = True
    while F:
        DistributeObrMinMax(TEST)
        CalcDist()
        if D < Dmean:
            break
        for j in range(Siz):
            ClustCntr[K, j] = TEST[Nvect, j]
        K += 1
        print(ClustersROW)
    DistributeObrMinMax(TEST)
    print(ClustersROW)
DrawAllLetters(1, 9, 0, 650, 0, 15, TEST)
IMG.show()
