import math
import numpy as np
from matplotlib import pyplot as plt

N = 50
rise = 0.1
kick = 0.05
oscillators = []
couplings = []
absb = 0
T = 1000
x1 = []
x2 = []
y1 = []
y2 = []
firing = []
N_abs = [0 for i in range(N)]
N_abs_old = [0 for i in range(N)]

def merger():
    taken = [False for i in range(len(couplings))]
    l = [set(elem) for elem in couplings]

    def dfs(node, index):
        taken[index] = True
        ret = node
        for i, item in enumerate(l):
            if not taken[i] and not ret.isdisjoint(item):
                ret.update(dfs(item, i))
        return ret

    couple = []
    for i, node in enumerate(l):
        if not taken[i]:
            couple.append(list(dfs(node, i)))
    return couple

class simple_oscillator():
    def __init__(self, val=0, ind=-1):
        self.val = val
        self.index = ind
        self.locked = [self]
        self.coupled = False
        self.kicked = False
        self.updated = False
        
    def check(self):
        if self.val >= 1.0:
            self.val = 0.0

    def firing(self):
        global kick
        self.lock(kick)

    def rise(self, rise):
        global kick
        global firing
        global couplings
        self.val += rise
        if self.val >= 1.0:
            firing.append(self)
            for i in self.locked:
                if i not in firing:
                    firing.append(i)

    def lock(self, kick):
        global N_abs
        global couplings
        global oscillators
        global absb
        for i in oscillators:
            if i != self:
                nvl = i.val + kick

                if nvl < 1.0:
                    i.kicked = True

                if nvl >= 1.0 and i not in self.locked:
                    print(self.index, i.index)
                    self.coupled = True
                    N_abs[self.index] += 1
                    N_abs[i.index] += 1
                    absb += 1
                    self.locked.append(i)
                    i.locked.append(self)
                    a = []
                    for j in i.locked:
                        if str(j.index) not in a:
                            a.append(str(j.index))
                    for j in self.locked:
                        if str(j.index) not in a:
                            a.append(str(j.index))
                    a = list(set(a))
                    couplings.append(a)
                elif nvl >= 1.0:
                    i.kicked = False    
                    #absb += 1

        couplings = merger()
        print(couplings)
        print(self.index, self.kicked, self.coupled, self.updated)

        if self.coupled:
            for var in couplings:
                if str(self.index) in var:
                    for k in var:
                        k = oscillators[int(k)]
                        k.val = 0.0
                        k.kicked = False
                        k.updated = True

        for i in oscillators:
            if i.kicked and not i.updated:
                i.val += kick 
        
for i in range(N):
    oscillators.append(simple_oscillator(np.random.random(), i))

for i in oscillators:
    couplings.append([str(i.index)])

for i in range(T):

    temp1 = 0.0
    temp2 = 0.0
    absb = 0
    firing = []
    
    print(i, N_abs)
    N_abs_old = N_abs
    for j in range(N):
        oscillators[j].coupled = False
        oscillators[j].kicked = False
        oscillators[j].updated = False
        print(oscillators[j].index, oscillators[j].val)

    for j in range(N):
        oscillators[j].rise(rise)

    for j in firing:
        j.updated = True
        j.firing()
    
    for j in range(N):
        oscillators[j].check()
        temp2 = temp2 + oscillators[j].val

    temp2 = temp2/N
    
    for j in range(N):
        temp1 = temp1 + (oscillators[j].val - temp2)**2
    temp1 = temp1/N

    x1.append(i)
    y1.append(temp1)
    if i % 1 == 0:
        x2.append(i)
        if temp1 < 0.1:
            y2.append(0)
        else:
            y2.append(absb)
        #print(N_abs, N_abs_old)
        #print(sum([N_abs[i] - N_abs_old[i] for i in range(N)])/2)
        #y2.append(sum([N_abs[i] - N_abs_old[i] for i in range(N)])/2)

#plt.subplot(2, 1, 1)
plt.plot(x1, y1, color='r', linewidth=0.8)
plt.xlabel('Timestep')
plt.ylabel('Variance')
#plt.subplots_adjust(wspace=0.3, hspace=0.4)
#plt.subplot(2, 1, 2)
#plt.xlabel('Timestep')
#plt.ylabel('Number of absorbtions')
#plt.plot(x2, y2, color='b', linewidth=1.25)
plt.show()
