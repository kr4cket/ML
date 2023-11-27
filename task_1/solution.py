import matplotlib as mlab
import math
import pylab

FILE = open('lab4.txt', 'r')
Arr = []
Arrk = []
ArrC = []
Num = 0
while True:
    s = FILE.readline()
    if len(s) == 0:
        break
    s = s.split(" ")
    if Num == 0:
        M = int(s[0])
        N = int(s[1])
    else:
        for i in range(4):
            Arr.append(int(s[i]))
    Num += 1

xmin = 0.0
xmax = 1.0

for i in range(4):
    Arrk.append((Arr[i + 4] - Arr[i]) / (xmax - xmin))
    ArrC.append(Arr[i] - Arrk[i] * xmin)

dx = 0.001
xlist = []
x = xmin
while x <= xmax:
    xlist.append(x)
    x = x + dx

for i in range(4):
    ylist = [Arrk[i] * x + ArrC[i] for x in xlist]
    pylab.plot(xlist, ylist, "-k")

ArrY = ArrC
ylist = []
xlist = []
dx = 0.001
x = 0
Xmax = 0
YMax = min(ArrC)
while x <= 1:
    ArrY = [Arrk[i] * x + ArrC[i] for i in range(4)]
    y = min(ArrY)
    xlist.append(x)
    ylist.append(y)
    if (y > YMax):
        YMax = y
        Xmax = x
    x += dx

pylab.plot(xlist, ylist, "-b")

p2 = Xmax
p1 = 1 - Xmax
print("%6.3f" % (YMax))
print("%6.3f %6.3f" % (p1, p2))
pylab.vlines(Xmax, ymin=0, ymax=YMax, color='g')
pylab.hlines(0, xmin=0, xmax=Xmax, color='r')
pylab.hlines(0, xmin=Xmax, xmax=1, color='y')
pylab.text(Xmax + 0.01, YMax / 2, "Game's Cost", color='k')
pylab.text(Xmax + 0.01, 0.1, "p1", color='k')
pylab.text(0.1, 0.1, "p2", color='k')
pylab.show()
