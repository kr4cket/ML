class FACTVAL:
    def __init__(self, s="noname", v=["no"] * 3):
        self.name = s
        self.numberValues = len(v)
        self.values = []
        for i in range(0, self.numberValues):
            self.values.append(v[i])

    def QUESTION(self, question):
        print(f"{question}\nВведите", end=" ")
        j = 0
        for i in range(0, self.numberValues - 2):
            print(f"{str(i + 1)}-({self.values[i]})", end=" ")
            j = i + 1
        print(f"{str(j + 1)}-({self.values[j]})", end=" ")
        print(f"{str(j + 2)}-({self.values[j + 1]}):", end=" ")


class Fact:
    def __init__(self, ob="no", v="no"):
        self.Object = ob
        self.value = v

    def Display(self):
        print(f"{self.Object} = {self.value}")

    def Get(self):
        return f"{self.Object} = {self.value}"


class Rule:
    NumberIf = 0
    Ifs = []
    then = Fact()

    def __init__(self, n=1, MasIf=[Fact()], th=Fact()):
        self.NumberIf = n
        self.Ifs = []
        for i in range(0, self.NumberIf):
            self.Ifs.append(MasIf[i])
        self.then = th

    def Display(self):
        print("Если ")
        for i in range(0, self.NumberIf):
            print(f"{self.Ifs[i].Get()}", end=" ")
            if i != self.NumberIf - 1:
                print("и", end=" ")
        print(f"\nТо {self.then.Get()}")


def Compute(nf, facts, nr, rules):
    f = True
    while f:
        f = False
        for i in range(0, nr):
            m = rules[i].NumberIf
            f1 = True
            for j in range(0, m):
                ss = rules[i].Ifs[j].Object
                sk = rules[i].Ifs[j].value
                f2 = False
                for k in range(0, nf):
                    s1 = facts[k].Object
                    if ss == s1:
                        s2 = facts[k].value
                        if sk != s2:
                            break
                        f2 = True
                        break
                if f2 == False:
                    f1 = False
                    break
                if f1 == False:
                    break
            if f1:
                ss = rules[i].then.Object
                sk = rules[i].then.value
                f3 = False
                for k in range(0, nf):
                    s1 = facts[k].Object
                    s2 = facts[k].value
                    if ss == s1:
                        if sk != s2:
                            print("\nПравила противоречивы.")
                            return -1
                        else:
                            f3 = True
                            break
                if f3 == False:
                    facts.append(Fact(ss, sk))
                    print(f"\nДоказано: {facts[nf].Get()}\nПо выполнению правила:")
                    rules[i].Display()
                    nf += 1
                    f = True
    if facts[nf - 1].Object == "оценка_продолжительности":
        return 1
    else:
        return 0


factvalues = []
nfv = 0
with open("factvalues.txt", encoding='utf-8') as file:
    while True:
        s = file.readline()
        if len(s) == 0:
            break
        s = s.split("=")
        s1 = s[0].split(" (")[1].split(")")[0]
        s2 = s[1].split(", ")
        s2[len(s2) - 1] = s2[len(s2) - 1].split("\n")[0]
        factvalues.append(FACTVAL(s1, s2))
        nfv += 1

questions = []
with open("questions.txt", encoding='utf-8') as file:
    while True:
        s = file.readline()
        if len(s) == 0:
            break
        s = s.split("=")[1].split("\n")[0]
        questions.append(s)

rules = []
nr = 0
with open("Rules.txt", encoding='utf-8') as file:
    while True:
        s = file.readline()
        if len(s) == 0:
            break
        if s == "если\n":
            mas_if = []
            n = 0
            s = file.readline()
            while True:
                s = s.split("=")
                s[1] = s[1].split("\n")[0]
                mas_if.append(Fact(s[0], s[1]))
                n += 1
                s = file.readline()
                if s[0:3] == "то ":
                    s = s.split("=")
                    s[0] = s[0].split("то ")[1]
                    s[1] = s[1].split("\n")[0]
                    th = Fact(s[0], s[1])
                    break
            rules.append(Rule(n, mas_if, th))
            nr += 1
            file.readline()
f = []
n = 0
for i in range(0, nfv):
    try:
        factvalues[i].QUESTION(questions[i])
        answ = int(input()) - 1
        f.append(Fact(factvalues[i].name, factvalues[i].values[answ]))
    except:
        print("Ошибка! Введите значение повторно!")
        factvalues[i].QUESTION(questions[i])
        answ = int(input()) - 1
        f.append(Fact(factvalues[i].name, factvalues[i].values[answ]))
    finally:
        n += 1
print("\nИсходные данные:\n")
for i in range(0, nf):
    f[i].Display()

Compute(n, f, nr, rules)
