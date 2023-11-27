FIRST_MODEL = 4
SECOND_MODEL = 5
THIRD_MODEL = 6
A_APPEAR_1 = 0
A_DISAPPEAR_1 = 0
A_APPEAR_2 = 0
A_DISAPPEAR_2 = 0
A_APPEAR_3 = 0
A_DISAPPEAR_3 = 0
B_APPEAR_1 = 0
B_DISAPPEAR_1 = 0
B_APPEAR_2 = 0
B_DISAPPEAR_2 = 0
B_APPEAR_3 = 0
B_DISAPPEAR_3 = 0

symbols = []


class Symbol:
    def __init__(self, arr):
        self.Array = arr

    def Display(self):
        res = '\n'.join(self.Array)
        print(res)

    def Get(self, i):
        return self.Array[i]


def FindCorner(arr):
    first_el = -1
    second_el = -1
    string = ''
    for i in range(6):
        for num in range(6):
            if arr[i][num] == '0' and num < 5 and arr[i][num + 1] == '*' and first_el == -1:
                first_el = num
                second_el = i + 1
                if num < 5 and arr[i][num + 1] == '*':
                    string = '00'
                    break
            if arr[i][num] == '0' and num == first_el and i == second_el:
                if arr[i][num] == '0' and arr[i][num + 1] == '0':
                    string = '000'
                    break

    if string == '000':
        return 1
    else:
        return 0


def FindRow(arr):
    for i in range(2):
        if '0000' in arr[i]:
            return 1
    return 0


def ReadFile():
    FILE = open('.txt', 'r')
    Temp = []
    Num = 0
    while True:
        s = FILE.readline()
        if len(s) == 0:
            break
        s = s.replace('\n', '')
        Temp.append(s)
        Num += 1
        if Num == 6:
            Num = 0
            symbols.append(Symbol(Temp))
            Temp = []


def FirstTask():
    global A_APPEAR_1
    global A_DISAPPEAR_1
    global A_APPEAR_2
    global A_DISAPPEAR_2
    global A_APPEAR_3
    global A_DISAPPEAR_3
    global B_APPEAR_1
    global B_DISAPPEAR_1
    global B_APPEAR_2
    global B_DISAPPEAR_2
    global B_APPEAR_3
    global B_DISAPPEAR_3
    print("Первый класс: В")
    temp = ""
    for i in range(6):
        for j in range(4):
            temp += symbols[j].Get(i) + "\t"
        temp += "\n"
    print(temp)
    print("Второй класс: О")
    temp = ""
    for i in range(6):
        for j in range(4, 9):
            temp += symbols[j].Get(i) + "\t"
        temp += "\n"
    print(temp)
    print("Третий класс: П")
    temp = ""
    for i in range(6):
        for j in range(9, 15):
            temp += symbols[j].Get(i) + "\t"
        temp += "\n"
    print(temp)

    print("Начальные вероятности: ")
    count_1 = 0
    for i in range(FIRST_MODEL):
        count_1 += FindCorner(symbols[i].Array)
    A_APPEAR_1 = count_1
    A_DISAPPEAR_1 = FIRST_MODEL - count_1
    count_2 = 0
    for i in range(4, SECOND_MODEL + 4):
        count_2 += FindCorner(symbols[i].Array)
    A_APPEAR_2 = count_2
    A_DISAPPEAR_2 = SECOND_MODEL - count_2
    count_3 = 0
    for i in range(9, THIRD_MODEL + 9):
        count_3 += FindCorner(symbols[i].Array)
    A_APPEAR_3 = count_3
    A_DISAPPEAR_3 = THIRD_MODEL - count_3

    print("""A: 0
   00""")
    print()
    print("B: 0000")
    print()
    print(f"P(H0) = {FIRST_MODEL}/{15} = {round(FIRST_MODEL / 15, 2)}")
    print(f"P(H1) = {SECOND_MODEL}/{15} = {round(SECOND_MODEL / 15, 2)}")
    print(f"P(H2) = {THIRD_MODEL}/{15} = {round(THIRD_MODEL / 15, 2)}")
    print()
    print(f"P(A/H0) = {count_1}/{FIRST_MODEL} = {round(count_1 / FIRST_MODEL, 2)}")
    print(f"P(A/H1) = {count_2}/{SECOND_MODEL} = {round(count_2 / SECOND_MODEL, 2)}")
    print(f"P(A/H2) = {count_3}/{THIRD_MODEL} = {round(count_3 / THIRD_MODEL, 2)}")

    count_1 = 0
    for i in range(FIRST_MODEL):
        count_1 += FindRow(symbols[i].Array)
    B_APPEAR_1 = count_1
    B_DISAPPEAR_1 = FIRST_MODEL - count_1
    count_2 = 0
    for i in range(4, SECOND_MODEL + 4):
        count_2 += FindRow(symbols[i].Array)
    B_APPEAR_2 = count_2
    B_DISAPPEAR_2 = SECOND_MODEL - count_2
    count_3 = 0
    for i in range(9, THIRD_MODEL + 9):
        count_3 += FindRow(symbols[i].Array)
    B_APPEAR_3 = count_3
    B_DISAPPEAR_3 = THIRD_MODEL - count_3
    print()
    print(f"P(B/H0) = {count_1}/{FIRST_MODEL} = {round(count_1 / FIRST_MODEL, 2)}")
    print(f"P(B/H1) = {count_2}/{SECOND_MODEL} = {round(count_2 / SECOND_MODEL, 2)}")
    print(f"P(B/H2) = {count_3}/{THIRD_MODEL} = {round(count_3 / THIRD_MODEL, 2)}")


def MAX(P1, P2, P3):
    if P1 >= P2 and P1 > P3:
        print(f"Ответ экспертной системы (B), вероятность = {round(P1, 2)}")
    elif P2 > P3:
        print(f"Ответ экспертной системы (О), вероятность = {round(P2, 2)}")
    else:
        print(f"Ответ экспертной системы (П), вероятность = {round(P3, 2)}")


def SecondTask():
    print("Первый образец: ")
    symbols[15].Display()
    print("~A~B - Элементы образцов отсутствуют вообще")
    print(f"P(~A/H0) = {A_DISAPPEAR_1}/{FIRST_MODEL} = {round(A_DISAPPEAR_1 / FIRST_MODEL, 2)}")
    print(f"P(~A/H1) = {A_DISAPPEAR_2}/{SECOND_MODEL} = {round(A_DISAPPEAR_2 / SECOND_MODEL, 2)}")
    print(f"P(~A/H2) = {A_DISAPPEAR_3}/{THIRD_MODEL} = {round(A_DISAPPEAR_3 / THIRD_MODEL, 2)}")
    temp = round(((A_DISAPPEAR_1 / FIRST_MODEL) * (FIRST_MODEL / 15)) + (
            (A_DISAPPEAR_2 / SECOND_MODEL) * (SECOND_MODEL / 15)) + (
                         (A_DISAPPEAR_3 / THIRD_MODEL) * (THIRD_MODEL / 15)), 2)
    print("P(~A) = ", temp)
    print(f"P(H0/~A) = P(~A/H0)*P(H0)/P(~A) = {round(((A_DISAPPEAR_1 / FIRST_MODEL) * (FIRST_MODEL / 15)) / temp, 2)}")
    print(
        f"P(H1/~A) = P(~A/H1)*P(H1)/P(~A) = {round(((A_DISAPPEAR_2 / SECOND_MODEL) * (SECOND_MODEL / 15)) / temp, 2)}")
    print(f"P(H2/~A) = P(~A/H2)*P(H2)/P(~A) = {round(((A_DISAPPEAR_3 / THIRD_MODEL) * (THIRD_MODEL / 15)) / temp, 2)}")

    print(f"P(~B/H0) = {B_DISAPPEAR_1}/{FIRST_MODEL} = {round(B_DISAPPEAR_1 / FIRST_MODEL, 2)}")
    print(f"P(~B/H1) = {B_DISAPPEAR_2}/{SECOND_MODEL} = {round(B_DISAPPEAR_2 / SECOND_MODEL, 2)}")
    print(f"P(~B/H2) = {B_DISAPPEAR_3}/{THIRD_MODEL} = {round(B_DISAPPEAR_3 / THIRD_MODEL, 2)}")
    temp = round(((B_DISAPPEAR_1 / FIRST_MODEL) * (FIRST_MODEL / 15)) + (
            (B_DISAPPEAR_2 / SECOND_MODEL) * (SECOND_MODEL / 15)) + (
                         (B_DISAPPEAR_3 / THIRD_MODEL) * (THIRD_MODEL / 15)), 2)
    print("P(~B) = ", temp)
    print(f"P(H0/~B) = P(~B/H0)*P(H0)/P(~B) = {round(((B_DISAPPEAR_1 / FIRST_MODEL) * (FIRST_MODEL / 15)) / temp, 2)}")
    print(
        f"P(H1/~B) = P(~B/H1)*P(H1)/P(~B) = {round(((B_DISAPPEAR_2 / SECOND_MODEL) * (SECOND_MODEL / 15)) / temp, 2)}")
    print(f"P(H2/~B) = P(~B/H2)*P(H2)/P(~B) = {round(((B_DISAPPEAR_3 / THIRD_MODEL) * (THIRD_MODEL / 15)) / temp, 2)}")
    MAX((((B_DISAPPEAR_1 / FIRST_MODEL) * (FIRST_MODEL / 15)) / temp),
        ((B_DISAPPEAR_2 / SECOND_MODEL) * (SECOND_MODEL / 15) / temp),
        ((B_DISAPPEAR_3 / THIRD_MODEL) * (THIRD_MODEL / 15)) / temp)

    print()

    print("Второй образец: ")
    symbols[16].Display()
    print("A~B - Элемент А присутсвует в списке, а В в списке отсутствет")
    print(f"P(A/H0) = {A_APPEAR_1}/{FIRST_MODEL} = {round(A_APPEAR_1 / FIRST_MODEL, 2)}")
    print(f"P(A/H1) = {A_APPEAR_2}/{SECOND_MODEL} = {round(A_APPEAR_2 / SECOND_MODEL, 2)}")
    print(f"P(A/H2) = {A_APPEAR_3}/{THIRD_MODEL} = {round(A_APPEAR_3 / THIRD_MODEL, 2)}")
    temp = round(
        ((A_APPEAR_1 / FIRST_MODEL) * (FIRST_MODEL / 15)) + ((A_APPEAR_2 / SECOND_MODEL) * (SECOND_MODEL / 15)) + (
                (A_APPEAR_3 / THIRD_MODEL) * (THIRD_MODEL / 15)), 2)
    print("P(A) = ", temp)
    print(f"P(H0/A) = P(A/H0)*P(H0)/P(A) = {round(((A_APPEAR_1 / FIRST_MODEL) * (FIRST_MODEL / 15)) / temp, 2)}")
    print(f"P(H1/A) = P(A/H1)*P(H1)/P(A) = {round(((A_APPEAR_2 / SECOND_MODEL) * (SECOND_MODEL / 15)) / temp, 2)}")
    print(f"P(H2/A) = P(A/H2)*P(H2)/P(A) = {round(((A_APPEAR_3 / THIRD_MODEL) * (THIRD_MODEL / 15)) / temp, 2)}")

    print(f"P(~B/H0) = {B_DISAPPEAR_1}/{FIRST_MODEL} = {round(B_DISAPPEAR_1 / FIRST_MODEL, 2)}")
    print(f"P(~B/H1) = {B_DISAPPEAR_2}/{SECOND_MODEL} = {round(B_DISAPPEAR_2 / SECOND_MODEL, 2)}")
    print(f"P(~B/H2) = {B_DISAPPEAR_3}/{THIRD_MODEL} = {round(B_DISAPPEAR_3 / THIRD_MODEL, 2)}")
    temp = round(((B_DISAPPEAR_1 / FIRST_MODEL) * (FIRST_MODEL / 15)) + (
            (B_DISAPPEAR_2 / SECOND_MODEL) * (SECOND_MODEL / 15)) + (
                         (B_DISAPPEAR_3 / THIRD_MODEL) * (THIRD_MODEL / 15)), 2)
    print("P(~B) = ", temp)
    print(f"P(H0/~B) = P(~B/H0)*P(H0)/P(~B) = {round(((B_DISAPPEAR_1 / FIRST_MODEL) * (FIRST_MODEL / 15)) / temp, 2)}")
    print(
        f"P(H1/~B) = P(~B/H1)*P(H1)/P(~B) = {round(((B_DISAPPEAR_2 / SECOND_MODEL) * (SECOND_MODEL / 15)) / temp, 2)}")
    print(f"P(H2/~B) = P(~B/H2)*P(H2)/P(~B) = {round(((B_DISAPPEAR_3 / THIRD_MODEL) * (THIRD_MODEL / 15)) / temp, 2)}")
    MAX(round(((B_DISAPPEAR_1 / FIRST_MODEL) * (FIRST_MODEL / 15)) / temp, 3),
        round(((B_DISAPPEAR_2 / SECOND_MODEL) * (SECOND_MODEL / 15)) / temp, 3),
        round(((B_DISAPPEAR_3 / THIRD_MODEL) * (THIRD_MODEL / 15)) / temp, 3))

    print()

    print("Третий образец: ")
    symbols[17].Display()
    print("~AB - Элемент В присутсвует в списке, а А в списке отсутствет")
    print(f"P(~A/H0) = {A_DISAPPEAR_1}/{FIRST_MODEL} = {round(A_DISAPPEAR_1 / FIRST_MODEL, 2)}")
    print(f"P(~A/H1) = {A_DISAPPEAR_2}/{SECOND_MODEL} = {round(A_DISAPPEAR_2 / SECOND_MODEL, 2)}")
    print(f"P(~A/H2) = {A_DISAPPEAR_3}/{THIRD_MODEL} = {round(A_DISAPPEAR_3 / THIRD_MODEL, 2)}")
    temp = round(((A_DISAPPEAR_1 / FIRST_MODEL) * (FIRST_MODEL / 15)) + (
            (A_DISAPPEAR_2 / SECOND_MODEL) * (SECOND_MODEL / 15)) + (
                         (A_DISAPPEAR_3 / THIRD_MODEL) * (THIRD_MODEL / 15)), 2)
    print("P(~A) = ", temp)
    print(f"P(H0/~A) = P(~A/H0)*P(H0)/P(~A) = {round(((A_DISAPPEAR_1 / FIRST_MODEL) * (FIRST_MODEL / 15)) / temp, 2)}")
    print(
        f"P(H1/~A) = P(~A/H1)*P(H1)/P(~A) = {round(((A_DISAPPEAR_2 / SECOND_MODEL) * (SECOND_MODEL / 15)) / temp, 2)}")
    print(f"P(H2/~A) = P(~A/H2)*P(H2)/P(~A) = {round(((A_DISAPPEAR_3 / THIRD_MODEL) * (THIRD_MODEL / 15)) / temp, 2)}")

    print(f"P(B/H0) = {B_APPEAR_1}/{FIRST_MODEL} = {round(B_APPEAR_1 / FIRST_MODEL, 2)}")
    print(f"P(B/H1) = {B_APPEAR_2}/{SECOND_MODEL} = {round(B_APPEAR_2 / SECOND_MODEL, 2)}")
    print(f"P(B/H2) = {B_APPEAR_3}/{THIRD_MODEL} = {round(B_APPEAR_3 / THIRD_MODEL, 2)}")
    temp = round(
        ((B_APPEAR_1 / FIRST_MODEL) * (FIRST_MODEL / 15)) + ((B_APPEAR_2 / SECOND_MODEL) * (SECOND_MODEL / 15)) + (
                (B_APPEAR_3 / THIRD_MODEL) * (THIRD_MODEL / 15)), 2)
    print("P(~B) = ", temp)
    print(f"P(H0/B) = P(B/H0)*P(H0)/P(B) = {round(((B_APPEAR_1 / FIRST_MODEL) * (FIRST_MODEL / 15)) / temp, 2)}")
    print(f"P(H1/B) = P(B/H1)*P(H1)/P(B) = {round(((B_APPEAR_2 / SECOND_MODEL) * (SECOND_MODEL / 15)) / temp, 2)}")
    print(f"P(H2/B) = P(B/H2)*P(H2)/P(B) = {round(((B_APPEAR_3 / THIRD_MODEL) * (THIRD_MODEL / 15)) / temp, 2)}")
    MAX(round(((B_APPEAR_1 / FIRST_MODEL) * (FIRST_MODEL / 15)) / temp, 2),
        round(((B_APPEAR_2 / SECOND_MODEL) * (SECOND_MODEL / 15)) / temp, 2),
        round(((B_APPEAR_3 / THIRD_MODEL) * (THIRD_MODEL / 15)) / temp, 2))

    print()

    print("Четвертый образец: ")
    symbols[18].Display()
    print("AB - Элемент А и В присутсвуют в образце")
    print(f"P(A/H0) = {A_APPEAR_1}/{FIRST_MODEL} = {round(A_APPEAR_1 / FIRST_MODEL, 2)}")
    print(f"P(A/H1) = {A_APPEAR_2}/{SECOND_MODEL} = {round(A_APPEAR_2 / SECOND_MODEL, 2)}")
    print(f"P(A/H2) = {A_APPEAR_3}/{THIRD_MODEL} = {round(A_APPEAR_3 / THIRD_MODEL, 2)}")
    temp = round(
        ((A_APPEAR_1 / FIRST_MODEL) * (FIRST_MODEL / 15)) + ((A_APPEAR_2 / SECOND_MODEL) * (SECOND_MODEL / 15)) + (
                (A_APPEAR_3 / THIRD_MODEL) * (THIRD_MODEL / 15)), 2)
    print("P(A) = ", temp)
    print(f"P(H0/A) = P(A/H0)*P(H0)/P(A) = {round(((A_APPEAR_1 / FIRST_MODEL) * (FIRST_MODEL / 15)) / temp, 2)}")
    print(f"P(H1/A) = P(A/H1)*P(H1)/P(A) = {round(((A_APPEAR_2 / SECOND_MODEL) * (SECOND_MODEL / 15)) / temp, 2)}")
    print(f"P(H2/A) = P(A/H2)*P(H2)/P(A) = {round(((A_APPEAR_3 / THIRD_MODEL) * (THIRD_MODEL / 15)) / temp, 2)}")

    print(f"P(B/H0) = {B_APPEAR_1}/{FIRST_MODEL} = {round(B_APPEAR_1 / FIRST_MODEL, 2)}")
    print(f"P(B/H1) = {B_APPEAR_2}/{SECOND_MODEL} = {round(B_APPEAR_2 / SECOND_MODEL, 2)}")
    print(f"P(B/H2) = {B_APPEAR_3}/{THIRD_MODEL} = {round(B_APPEAR_3 / THIRD_MODEL, 2)}")
    temp = round(
        ((B_APPEAR_1 / FIRST_MODEL) * (FIRST_MODEL / 15)) + ((B_APPEAR_2 / SECOND_MODEL) * (SECOND_MODEL / 15)) + (
                (B_APPEAR_3 / THIRD_MODEL) * (THIRD_MODEL / 15)), 2)
    print("P(~B) = ", temp)
    print(f"P(H0/B) = P(B/H0)*P(H0)/P(B) = {round(((B_APPEAR_1 / FIRST_MODEL) * (FIRST_MODEL / 15)) / temp, 2)}")
    print(f"P(H1/B) = P(B/H1)*P(H1)/P(B) = {round(((B_APPEAR_2 / SECOND_MODEL) * (SECOND_MODEL / 15)) / temp, 2)}")
    print(f"P(H2/B) = P(B/H2)*P(H2)/P(B) = {round(((B_APPEAR_3 / THIRD_MODEL) * (THIRD_MODEL / 15)) / temp, 2)}")
    MAX(round(((B_APPEAR_1 / FIRST_MODEL) * (FIRST_MODEL / 15)) / temp, 2),
        round(((B_APPEAR_2 / SECOND_MODEL) * (SECOND_MODEL / 15)) / temp, 2),
        round(((B_APPEAR_3 / THIRD_MODEL) * (THIRD_MODEL / 15)) / temp, 2))


ReadFile()
FirstTask()
SecondTask()
