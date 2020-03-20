from random import random, randint, uniform
from math import log, e


breakup = {
    (12, 15): 0.0815,
    (15, 21): 0.0415,
    (21, 35): 0.0415,
    (35, 45): 0.0208,
    (45, 60): 0.0105,
    (60, 125): 0.0052
}

deathM = {
    (0, 12): 0.25,
    (12, 45): 0.1,
    (45, 76): 0.3,
    (76, 125): 0.7
}

deathF = {
    (0, 12): 0.25,
    (12, 45): 0.15,
    (45, 76): 0.35,
    (76, 125): 0.65
}

pregnant = {
    (12, 15): 0.2,
    (15, 21): 0.45,
    (21, 35): 0.8,
    (35, 45): 0.4,
    (45, 60): 0.2,
    (60, 125): 0.05
}

children_number = {
    1: 0.6,
    2: 0.75,
    3: 0.35,
    4: 0.2,
    5: 0.1,
    6: 0.05
}

wish_couple = {
    (12, 15): 0.6,
    (15, 21): 0.65,
    (21, 35): 0.8,
    (35, 45): 0.6,
    (45, 60): 0.5,
    (60, 125): 0.2
}

make_couple = {
    (0, 5): 0.45,
    (5, 10): 0.4,
    (10, 15): 0.35,
    (15, 20): 0.25,
    (20, 100): 0.15
}

children_born = {
    1: 0.7,
    2: 0.18,
    3: 0.08,
    4: 0.04,
    5: 0.02
}


def exponential(lamb, u):
    return -log(u) / lamb


def poissonHomogeneous(lamb, t):         
    accum = 1                   
    n = 0               
    data = [0]                                           
    while True:
        u = random()  
        accum *= u 
        ex = exponential(lamb, u)
        data.append(ex + data[len(data) - 1])
        n += 1
        if (-log(accum)/lamb) > t:
            return n, data


def generateTimesU(length):
    times = [0]
    while True:
        u = randint(0, length)
        times.append(times[-1] + u)
        if times[-1] >= 4800:
            return times
        

def generateTimesP(lamb, top):
    accum = 0
    last = 0
    times = [0]
    while True:
        _, data = poissonHomogeneous(lamb, top)
        for i in data[1:]:
            times.append(int(last + i))
            if last + i >= 4800:
                return times
        accum += data[-1]
        last = accum
    

def generateTimes(kind, *args):
    if kind == "Poisson":
        return generateTimesP(*args)
    elif kind == "Uniform":
        generateTimesU(*args)
