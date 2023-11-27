from tkinter import *
import math
import pylab
from matplotlib import mlab
import numpy as np
import codecs

namesVars, namesTerms = [], []
amountOfTerms = np.zeros((10), dtype=int)
amountOfIntervals = np.zeros((10, 10), dtype=int)
intervals = np.zeros((10, 10, 10), dtype=np.float64)  # интервалы: intervals[переменная, терм, номер]
rightEnd = np.zeros((10, 10, 10), dtype=np.float64)  # правый конец
valueOnLeft = np.zeros((10, 10, 10), dtype=np.float64)  # значение на левом конце
valueOnRight = np.zeros((10, 10, 10), dtype=np.float64)  # значение на правом конце
fuzzTerms = np.zeros((10, 10), dtype=np.float64)  # фаззификация каждого терма fuzzTerms[i][j] - переменная терм
toFuzzy = np.zeros((10), dtype=np.float64)  # исходные значения для фаззификации
agr = np.zeros((100), dtype=np.float64)
activatedX = np.zeros((100, 1000), dtype=np.float64)  # результат активации по X
activatedY = np.zeros((100, 1000), dtype=np.float64)  # результат активации по Y
accumX = np.zeros((1000), dtype=np.float64)  # результат аккумуляции по X
accumY = np.zeros((1000), dtype=np.float64)  # результат аккумуляции по Y


def inputData():
    global amountVar
    f = codecs.open('D:/input.txt', 'r', 'utf_8_sig')
    s = f.readline()
    amountVar = int(s)
    for i in range(0, amountVar):
        s = f.readline()
        namesVars.append(s)
        s = f.readline()
        k = int(s)
        amountOfTerms[i] = k
        for j in range(0, k):
            s = f.readline()
            namesTerms[i][j] = s
            s = f.readline()
            n = int(s)
            amountOfIntervals[i, j] = n
            for p in range(0, n):
                s = f.readline()
                s1 = s.split(' ')
                s2 = s1[0]
                s2 = float(s2)
                intervals[i, j, p] = s2;
                s2 = s1[1]
                s2 = float(s2)
                rightEnd[i, j, p] = s2;
                s2 = s1[2]
                s2 = float(s2)
                valueOnLeft[i, j, p] = s2;
                s2 = s1[3]
                s2 = float(s2)
                valueOnRight[i, j, p] = s2;
    return


def fuzzy():
    formFuzzy = Toplevel()
    formFuzzy.title("Фаззификация")
    formFuzzy.geometry("550x420")  # размер формы
    var1 = IntVar()  # для радиокнопок
    lb4 = Label(formFuzzy, text="Просмотр", anchor=W)
    lb4.place(x=270, y=10, width=80, height=25)
    R1 = Radiobutton(formFuzzy, text="Температура", variable=var1, value=1, anchor=W)
    R1.place(x=270, y=40, width=150, height=25)
    R2 = Radiobutton(formFuzzy, text="Скорость", variable=var1, value=2, anchor=W)
    R2.place(x=270, y=70, width=150, height=25)
    R1.select()
    lb1 = Label(formFuzzy, text="Температура:", anchor=W)
    lb1.place(x=10, y=10, width=150, height=25)
    En1 = Entry(formFuzzy)  # текстовое поле ввода
    En1.place(x=160, y=10, width=80, height=25)
    lb2 = Label(formFuzzy, text="Скорость изменения:", anchor=W)
    lb2.place(x=10, y=50, width=150, height=25)
    En2 = Entry(formFuzzy)
    En2.place(x=160, y=50, width=80, height=25)
    scrollbar = Scrollbar(formFuzzy)  # скроллинг для listbox
    scrollbar.pack(side=RIGHT, fill=Y)
    lx1 = Listbox(formFuzzy, height=15, width=45, selectmode=SINGLE)
    lx1.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=lx1.yview)
    lx1.place(x=180, y=140)
    bt1 = Button(formFuzzy, text="Задать", command=lambda: displayFuzzy(En1, En2, lx1, var1))
    # функция, вызываемая при нажатии кнопки
    bt1.place(x=40, y=140, width=120)
    formFuzzy.mainloop()


def displayFuzzy(En1, En2, lx1, var1):  # функция фаззификации при нажатии кнопки Задать
    global numOfGraph
    inputData()  # чтение всех интервалов
    s1 = En1.get()
    x1 = float(s1)
    s1 = En2.get()
    x2 = float(s1)
    k = var1.get()
    for i in range(0, amountVar - 1):  # цикл по входным переменным
        s = namesVars[i]
        if (i == 0):
            xx = x1
        if (i == 1):
            xx = x2
        lx1.insert(END, s)  # имя переменной в listbox
        # интерполяция по каждому терму i переменной
        n = amountOfTerms[i]  # число термов у i переменной
        # цикл по термам переменной i
        ss = ""
        for j in range(0, n):
            s = namesTerms[i][j]
            t = amountOfIntervals[i][j]  # число интервалов у j-терма i переменной
            fuzzTerms[i][j] = 0  # результат фаззификации
            for v in range(0, t):  # цикл по интервалам
                Lg = intervals[i][j][v]
                Rg = rightEnd[i][j][v]
                Bg = valueOnLeft[i][j][v]
                Eg = valueOnRight[i][j][v]
                if (xx > Lg and xx < Rg):
                    fuzzTerms[i][j] = (Eg - Bg) * (xx - Lg) / (Rg - Lg) + Bg  # интерполяция
                    w = fuzzTerms[i][j] * 100  # округление до 0.01
                    r = math.trunc(w)
                    w = r / 100
                    fuzzTerms[i][j] = w
            s1 = str(fuzzTerms[i][j])
            s = s + " " + s1
            ss = ss + s + " "
            lx1.insert(END, ss)
    global numOfFuzzDisp
    if (k == 1):
        numOfFuzzDisp = 1
        numOfGraph = 0  # график емкости
    if (k == 2):
        numOfFuzzDisp = 2
        numOfGraph = 1  # график расхода
    toFuzzy[0] = x1
    toFuzzy[1] = x2
    displayGraph()
    return


def agregate():  # отклик на выбор пункта еню Агрегирование
    formAgregate = Toplevel()  # форма для агрегирования
    formAgregate.title("Агрегирование")
    formAgregate.geometry("600x300")  # размер формы
    s1 = 'Температура: '
    s = str(toFuzzy[0])
    s1 = s1 + s
    lb1 = Label(formAgregate, text=s1, anchor=W)
    lb1.place(x=10, y=10, width=170, height=25)
    s1 = 'Скорость: '
    s = str(toFuzzy[1])
    s1 = s1 + s
    lb4 = Label(formAgregate, text=s1, anchor=W)
    lb4.place(x=10, y=50, width=170, height=25)
    lb3 = Label(formAgregate, text="Выбор функции AND", anchor=W)
    lb3.place(x=190, y=10, width=140, height=25)
    bt1 = Button(formAgregate, text="Агрегирование", command=lambda: displayAgregate(var1, lx1))  # функция, при нажатии
    bt1.place(x=30, y=150, width=200)
    var1 = IntVar()  # для радиокнопок
    R1 = Radiobutton(formAgregate, text="Минимум", variable=var1, value=1, anchor=W)
    R1.place(x=190, y=40, width=140, height=25)
    R2 = Radiobutton(formAgregate, text="Умножение", variable=var1, value=2, anchor=W)
    R2.place(x=190, y=70, width=140, height=25)
    R1.select()
    lx1 = Listbox(formAgregate, height=12, width=20, selectmode=SINGLE)
    lx1.place(x=350, y=20)
    formAgregate.mainloop()
    return


def displayAgregate(var1, lx1):
    global amountVar
    global amountOfRules
    k = var1.get()

    numOfRule = 0  # № правила
    agr[numOfRule] = 1.0
    N1 = amountOfTerms[0]
    N2 = amountOfTerms[1]
    for i1 in range(0, N1):
        for i2 in range(0, N2):
            if (k == 1):
                if (fuzzTerms[0][i1] < agr[numOfRule]):
                    agr[numOfRule] = fuzzTerms[0][i1]
                if (fuzzTerms[1][i2] < agr[numOfRule]):
                    agr[numOfRule] = fuzzTerms[1][i2]
            else:
                agr[numOfRule] = agr[numOfRule] * fuzzTerms[0][i1]
                agr[numOfRule] = agr[numOfRule] * fuzzTerms[1][i2]
            numOfRule = numOfRule + 1
            agr[numOfRule] = 1.0
    agr[14] = 1.0

    lx1.insert(0, "Правила")
    for i in range(0, 15):
        s = str(i + 1)
        s = "Правило: " + s
        s1 = str(agr[i])
        s = s + " "
        s = s + s1
        lx1.insert(END, s)
    return


def activate():
    formActivate = Toplevel()
    formActivate.title("Активирование")
    formActivate.geometry("600x350")  # размер формы
    lx1 = Listbox(formActivate, height=12, width=55, selectmode=SINGLE)
    lx1.place(x=10, y=20)
    lx1.insert(0, "Правила")
    for i in range(0, 15):
        s = str(i + 1)
        s = "Правило: " + s
        s1 = str(agr[i])
        s = s + " "
        s = s + s1
        s1 = " Режим работы"
        if (i < 6):
            s1 = s1 + "=тепло"
        if (i >= 6 and i < 9):
            s1 = s1 + "=не включать"
        if (i > 9):
            s1 = s1 + "=холодно"
        s = s + s1
        lx1.insert(END, s)
    lb1 = Label(formActivate, text="Выбор функции AND", anchor=W)
    lb1.place(x=360, y=10, width=200, height=25)
    var1 = IntVar()  # для радиокнопок
    R1 = Radiobutton(formActivate, text="Минимум", variable=var1, value=1, anchor=W)
    R1.place(x=360, y=40, width=140, height=25)
    R2 = Radiobutton(formActivate, text="Умножение", variable=var1, value=2, anchor=W)
    R2.place(x=360, y=70, width=140, height=25)
    R1.select()
    amountOfActiv = 1000
    bt1 = Button(formActivate, text="Построение", command=lambda: calcActivate(var1, lx1, amountOfActiv))
    bt1.place(x=360, y=110, width=190)
    Nr = 0
    bt2 = Button(formActivate, text="Просмотр", command=lambda: displayActivate(Nr, lx1, amountOfActiv))
    bt2.place(x=360, y=160, width=190)
    formActivate.mainloop()
    return


def displayActivate(Nr, lx1, amountOfActiv):
    xlist = []
    ylist = []
    s = lx1.curselection()
    Nr = s[0] - 1  # выбранный номер в listbox
    for i in range(0, amountOfActiv - 1):
        xlist.append(activatedX[Nr][i])
        ylist.append(activatedY[Nr][i])
    pylab.plot(xlist, ylist, "-m")
    pylab.show()
    return


def calcActivate(var1, lx1, amountOfActiv):
    numOfTermsInOut = -1  # номер терма в выходной переменной в i правиле
    N = 1000  # шаг построения
    for i in range(0, 15):
        s = lx1.get(i + 1)
        m = s.find("тепло")
        if (m > 0):
            numOfTermsInOut = 0
        m = s.find("не включать")
        if (m > 0):
            numOfTermsInOut = 1
        m = s.find("холод")
        if (m > 0):
            numOfTermsInOut = 2
        Xmin = intervals[2][numOfTermsInOut][0]
        Xmax = Xmin
        z = amountOfIntervals[2][numOfTermsInOut]  # работа с вых.переменной(2) и с соотв. термом в правиле
        for y in range(0, z):
            if (rightEnd[2][numOfTermsInOut][y] > Xmax):
                Xmax = rightEnd[2][numOfTermsInOut][y]
        dx = (Xmax - Xmin) / amountOfActiv
        q = 0
        x = Xmin
        while (q < amountOfActiv - 1):  # построение точек графика
            u = -1
            for r in range(0, z):
                if (x >= intervals[2][numOfTermsInOut][r] - 0.00001 and x < rightEnd[2][numOfTermsInOut][r]):
                    u = r
                    break
            if (u >= 0):
                activatedX[i][q] = x
                y = (x - intervals[2][numOfTermsInOut][u]) / (
                        rightEnd[2][numOfTermsInOut][u] - intervals[2][numOfTermsInOut][u])
                y = y * (valueOnRight[2][numOfTermsInOut][u] - valueOnLeft[2][numOfTermsInOut][u]) + \
                    valueOnLeft[2][numOfTermsInOut][u]
                activatedY[i][q] = y
            x = x + dx
            q = q + 1
            # активизация
        for i in range(0, 15):
            v = agr[i]
            q = 0
            k = var1.get()
            while (q < amountOfActiv - 1):
                if (k == 1):
                    # минимум
                    if (v < activatedY[i][q]):
                        activatedY[i][q] = v
                else:
                    activatedY[i][q] = v * activatedY[i][q]  # умножение
                q = q + 1

    return


def accumulate():
    formAccumulate = Toplevel()
    formAccumulate.title("Аккумуляция")
    formAccumulate.geometry("250x170")  # размер формы
    lb1 = Label(formAccumulate, text="Выбор функции OR", anchor=W)
    lb1.place(x=30, y=10, width=200, height=25)
    var1 = IntVar()  # для радиокнопок
    R1 = Radiobutton(formAccumulate, text="Максимум", variable=var1, value=1, anchor=W)
    R1.place(x=30, y=40, width=140, height=25)
    R2 = Radiobutton(formAccumulate, text="Сложение", variable=var1, value=2, anchor=W)
    R2.place(x=30, y=70, width=140, height=25)
    R1.select()
    Naccum = 1000
    bt1 = Button(formAccumulate, text="Аккумуляция", command=lambda: displayAccumulate(var1, Naccum))
    bt1.place(x=30, y=110, width=190)
    formAccumulate.mainloop()
    return


def displayAccumulate(var1, Naccum):
    k = var1.get()
    for i in range(0, Naccum - 1):
        x = activatedX[0][i]
        y = activatedY[0][i]
        for j in range(1, 15):
            if (k == 1):  # максимум
                if (activatedY[j][i] > y):
                    y = activatedY[j][i]
            else:
                y = y + activatedY[j][i] - y * activatedY[j][i]  # сумма
        accumX[i] = x
        accumY[i] = y
    xlist = []
    ylist = []
    for i in range(0, Naccum - 1):  # график
        xlist.append(accumX[i])
        ylist.append(accumY[i])
        pylab.plot(xlist, ylist, "-m")
    pylab.show()
    return


def unfuzzy():
    amountOfUnfuzzy = 1000
    S1 = 0
    S2 = 0
    for i in range(0, amountOfUnfuzzy - 1):
        S1 = S1 + accumY[i] * accumX[i]
        S2 = S2 + accumY[i]
    V = S1 / S2
    print("Значение работы кондиционера: ", V)
    return


def displayGraph():
    dx = 0.01
    global numOfGraph  # 0,1,2 номер переменной
    global numOfFuzzDisp
    Nr = numOfGraph
    Ng = amountOfTerms[Nr]
    print(Ng)
    for j in range(0, Ng):
        Ni = amountOfIntervals[Nr, j]
        for q in range(0, Ni):
            Xmin = intervals[Nr, j, q]
            Xmax = rightEnd[Nr, j, q]
            xlist = []
            x = Xmin
            while x <= Xmax + 0.0001:  # особенность вещественной арифметики
                xlist.append(x)
                x = x + dx
            k = (valueOnRight[Nr, j, q] - valueOnLeft[Nr, j, q]) / (rightEnd[Nr, j, q] - intervals[Nr, j, q])
            c = valueOnLeft[Nr, j, q] - k * intervals[Nr, j, q]
            ylist = [k * x + c for x in xlist]
            if (j == 0):
                pylab.plot(xlist, ylist, "-b")
                if (q == 0):
                    s = namesTerms[Nr][q]
                    pylab.text(intervals[Nr, j, q] + 0.15, -0.15, s, color='b')
            if (j == 1):
                pylab.plot(xlist, ylist, "-g")
                if (q == 1):
                    s = namesTerms[Nr][q]
                    pylab.text(intervals[Nr, j, q] + 0.15, -0.15, s, color='g')
            if (j == 2):
                pylab.plot(xlist, ylist, "-r")
                if (q == 2):
                    s = namesTerms[Nr][q]
                    pylab.text(intervals[Nr, j, q] + 0.15, -0.15, s, color='r')
            if (j == 3):
                pylab.plot(xlist, ylist, "-k")
                if (q == 3):
                    s = namesTerms[Nr][q]
                    pylab.text(intervals[Nr, j, q] + 0.15, -0.15, s, color='k')
            if (j == 4):
                pylab.plot(xlist, ylist, "-y")
                if (q == 4):
                    s = namesTerms[Nr][q]
                    pylab.text(intervals[Nr, j, q] + 0.15, -0.15, s, color='y')
    if (numOfFuzzDisp == 0):  # обычный просмотр
        pylab.show()
    Ng = amountOfTerms[Nr]  ##дополнительные линии фаззификации
    for i in range(0, Ng):
        # горизонтальные отрезки
        xlist = []
        xlist.append(intervals[Nr][i][0])
        xlist.append(toFuzzy[Nr])
        c = fuzzTerms[Nr][i]
        ylist = [c for x in xlist]
        if (i == 0):
            pylab.plot(xlist, ylist, "-b")
        if (i == 1):
            pylab.plot(xlist, ylist, "-g")
        if (i == 2):
            pylab.plot(xlist, ylist, "-r")
        # вертикальные отрезки
        xlist1 = []
        xlist1.append(toFuzzy[Nr])
        xlist1.append(toFuzzy[Nr])
        c = fuzzTerms[Nr][i]
        ylist1 = []
        ylist1.append(0)
        ylist1.append(c)
        if (i == 0):
            pylab.plot(xlist1, ylist1, "-b")
        if (i == 1):
            pylab.plot(xlist1, ylist1, "-g")
        if (i == 2):
            pylab.plot(xlist1, ylist1, "-r")
    pylab.show()
    return


def displayGovSupp():
    global numOfGraph
    global numOfFuzzDisp
    numOfFuzzDisp = 0
    inputData()
    numOfGraph = 0
    displayGraph()
    return


def displayInvest():
    global numOfGraph
    global numOfFuzzDisp
    numOfFuzzDisp = 0
    inputData()
    numOfGraph = 1
    displayGraph()
    return


def displayInnovation():
    global numOfGraph
    global numOfFuzzDisp
    numOfFuzzDisp = 0
    inputData()
    numOfGraph = 2
    displayGraph()
    return


def displayCompetitive():
    global numOfGraph
    global numOfFuzzDisp
    numOfFuzzDisp = 0
    inputData()
    numOfGraph = 3
    displayGraph()
    return


def displayRules():
    formRules = Tk()
    formRules.minsize(300, 400)
    scrollbar = Scrollbar(formRules)
    scrollbar.pack(side=RIGHT, fill=Y)
    lx1 = Listbox(formRules, height=24, width=45, selectmode=SINGLE)
    lx1.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=lx1.yview)
    lx1.place(x=10, y=20)
    lx1.pack()
    file1 = codecs.open('D:/rules.txt', 'r', 'utf_8_sig')
    lines = file1.readlines()
    # итерация по строкам
    for line in lines:
        lx1.insert(END, line)
    # закрываем файл
    file1.close
    formRules.mainloop()
    return


def exit():
    root.destroy()


root = Tk()
root.minsize(550, 300)
mainmenu = Menu(root)
root.config(menu=mainmenu)
filemenu = Menu(mainmenu, tearoff=0)
filemenu.add_command(label='Температура в помещении', command=displayGovSupp)
filemenu.add_command(label='Скорость изменения температуры', command=displayInvest)
filemenu.add_command(label='Режим работы кондиционера', command=displayInnovation)
filemenu.add_command(label='Правила', command=displayRules)
filemenu.add_command(label='Выход', command=exit)
mainmenu.add_cascade(label='Просмотр', menu=filemenu)
mainmenu.add_command(label='Фаззификация', command=fuzzy)
mainmenu.add_command(label="Агрегирование", command=agregate)
mainmenu.add_command(label="Активизация", command=activate)
mainmenu.add_command(label="Аккумуляция", command=accumulate)
mainmenu.add_command(label="Дефаззификация", command=unfuzzy)
namesTerms = [[''] * 5 for i in range(5)]
root.mainloop()
