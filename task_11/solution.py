import codecs


class rule:
    If = ''
    Then = ''

    def __init__(self, a, b):
        self.If = a
        self.Then = b

    def display(self):
        s = "Если "
        s = s + self.If
        s = s + "То "
        s = s + self.Then
        print(s)


rules = []
f = codecs.open('FILE.txt', 'r', encoding="utf-8")
while True:
    s1 = f.readline()
    if len(s1) == 0:
        break
    s2 = f.readline()
    c = rule(s1, s2)
    rules.append(c)
f.close()
k = len(rules)
for i in range(0, k):
    rules[i].display()

print('\n')
Proven = []
Nproven = 0
Proven.append("хороший муж\r\n")
Nproven = 1
Nrules = len(rules)
F = True
while (F):
    F = False
    for i in range(0, Nproven):
        s1 = Proven[i]
        for j in range(0, Nrules):
            s2 = rules[j].If
            if (s1 == rules[j].If):
                s1 = rules[j].Then
                F1 = True
                for m in range(0, Nproven):
                    s2 = Proven[m]
                    if (s1 == s2):
                        F1 = False
                        break
                if (F1):
                    Nproven = Nproven + 1
                    Proven.append(s1)
                    s = "Доказано: " + s1
                    print(s)
                    s = "Из правила"
                    print(s)
                    s = "Если "
                    s = s + rules[j].If
                    s = s + "То "
                    s = s + rules[j].Then
                    print(s)
                    F = True
