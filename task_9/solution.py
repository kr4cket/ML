import random
import numpy as np


def PcNew(PC, PY, PN, Answer):
    if Answer > 0:
        znam = PY * PC + PN * (1 - PC)
        if znam == 0:
            PY -= 0.0001
            PC -= 0.0001
        Pp = PY * PC / (PY * PC + PN * (1 - PC))
        if Answer == 5:
            return Pp
        return Answer / 5 * (Pp - PC) + PC
    if Answer < 0:
        znam = (1 - PY) * PC + (1 - PN) * (1 - PC)
        if znam == 0:
            PY -= 0.0001
            PC -= 0.0001
        Pm = (1 - PY) * PC / ((1 - PY) * PC + (1 - PN) * (1 - PC))
        if Answer == -5:
            return Pm
        return Answer / 5 * (PC - Pm) + PC
    return PC


disease_name = []
disease_num = []
disease_count = 0
flag_disease = []
kol_disease = []
index_max_disease = []
questions = []
symp_num = []
symp_count = 0
flag_symp = []
P0 = []
Py = []
Pn = []
connect_count = 0
Pc = []
PcMin = []
PcMax = []
prove = []

f = open('diseases.txt', 'r')
while True:
    s = f.readline()
    if len(s) == 0:
        break
    disease_name.append(s.split('\n')[0])
    disease_count += 1
    P0.append(float(f.readline()))
    s = f.readline()
    while s != '999\n':
        s1 = s.split(' ')
        disease_num.append(disease_count)
        symp_num.append(int(s1[0]))
        Py.append(float(s1[1]))
        Pn.append(float(s1[2]))
        connect_count += 1
        s = f.readline()
f.close

f = open('symptoms.txt', 'r')
while True:
    s = f.readline()
    if len(s) == 0:
        break
    questions.append(s.split('\n')[0])
    symp_count += 1
f.close

for i in range(0, disease_count):
    flag_disease.append(True)
    Pc.append(P0[i])
    PcMin.append(0)
    PcMax.append(0)
for i in range(0, symp_count):
    flag_symp.append(True)
    kol_disease.append(0)
    prove.append(False)
    index_max_disease.append(False)

flag_end = True
flag_one_disease = True
num_quest = 1
print('В качестве ответов числа от -5 до 5.')

while flag_end:
    for i in range(0, symp_count):
        kol_disease[i] = 0
    for i in range(0, connect_count):
        z = symp_num[i] - 1
        if flag_symp[z]:
            v = disease_num[i] - 1
            if flag_disease[v]:
                kol_disease[z] += 1
    max_disease_symp = 0
    count_max_disease = 0
    for i in range(0, symp_count):
        index_max_disease[i] = False
    for i in range(0, symp_count):
        if flag_symp[i]:
            if kol_disease[i] > max_disease_symp:
                max_disease_symp = kol_disease[i]
                count_max_disease = 1
                for j in range(0, i):
                    index_max_disease[j] = False
                index_max_disease[i] = True
            else:
                if kol_disease[i] == max_disease_symp:
                    count_max_disease += 1
                    index_max_disease[i] = True
    if count_max_disease == 1:
        for i in range(0, symp_count):
            if index_max_disease[i]:
                Nq = i
                break
    else:
        m = 0
        z = random.randint(0, count_max_disease - 1)
        for i in range(0, symp_count):
            if index_max_disease[i]:
                if z == m:
                    Nq = i
                    break
                m += 1
    flag_symp[Nq] = False
    answer = int(input(str(num_quest) + ". " + questions[Nq] + " "))
    for i in range(0, connect_count):
        z = symp_num[i] - 1
        if z == Nq:
            v = disease_num[i] - 1
            if flag_disease[v]:
                PC = P0[v]
                PY = Py[i]
                PN = Pn[i]
                P0[v] = PcNew(PC, PY, PN, answer)
    num_quest += 1
    max1 = -1
    imax1 = -1
    for i in range(0, disease_count):
        if flag_disease[i] and P0[i] > max1:
            max1 = P0[i]
            imax1 = i
    if flag_one_disease:
        vrem = max1
        P0[imax1] = 0
        max2 = -1
        imax2 = -1
        for i in range(0, disease_count):
            if flag_disease[i] and P0[i] > max2:
                max2 = P0[i]
                imax2 = i
        P0[imax1] = vrem
        print("На данный момент основной диагноз - " + disease_name[imax1] +
              " (c вероятностью: %.3f" % P0[imax1] + "), альтернативa - " +
              disease_name[imax2] + " (вероятность: %.3f" % P0[imax2] + ")")
    else:
        print("На данный момент основной диагноз - " + disease_name[imax1] +
              " (вероятность: %.3f" % P0[imax1] + ").")
    for i in range(0, disease_count):
        PcMin[i] = P0[i]
        PcMax[i] = P0[i]
    for i in range(0, connect_count):
        z = disease_num[i] - 1
        v = symp_num[i] - 1
        if flag_disease[z] and flag_symp[v]:
            PcCur = np.float64(PcMax[z])
            PY = np.float64(Py[i])
            PN = np.float64(Pn[i])
            pPlusMax = PcNew(PcCur, PY, PN, 5)
            pMinusMax = PcNew(PcCur, PY, PN, -5)
            PcCur = np.float64(PcMin[z])
            pPlusMin = PcNew(PcCur, PY, PN, 5)
            pMinusMin = PcNew(PcCur, PY, PN, -5)
            PcMin[z] = min(pPlusMax, pMinusMax, pPlusMin, pMinusMin)
            PcMax[z] = max(pPlusMax, pMinusMax, pPlusMin, pMinusMin)
    for i in range(0, disease_count):
        for j in range(0, disease_count):
            if flag_disease[i] and flag_disease[j]:
                if PcMin[i] > PcMax[j]:
                    flag_disease[j] = False
                    print("              " + disease_name[j] + " - исключена")
    now_count_disease = 0
    for i in range(0, disease_count):
        if flag_disease[i]:
            now_count_disease += 1
    if now_count_disease == 1:
        flag_one_disease == False
    for i in range(0, connect_count):
        z = disease_num[i] - 1
        v = symp_num[i] - 1
        if flag_disease[z]:
            prove[v] = True
    flag_end = False
    for i in range(0, symp_count):
        if prove[i] == False:
            flag_symp[i] = False
    for i in range(0, symp_count):
        if flag_symp[i]:
            flag_end = True
    for i in range(0, symp_count):
        prove[i] = False
    kols = 0
    for i in range(0, symp_count):
        if flag_symp[i] == False:
            kols += 1
    kolb = 0
    for i in range(0, disease_count):
        if flag_disease[i] == False:
            kolb += 1

for i in range(0, disease_count):
    if flag_disease[i]:
        print("Окончательный диагноз - " + disease_name[i] + " с вероятностью %.3f" % P0[i] + ".")
