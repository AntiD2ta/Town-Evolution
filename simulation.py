import utils, time
from utils import LoggerFactory as Logger

log = Logger(name='Simulator')


class Person:

    def __init__(self, sex, age):
        self.sex = sex
        self.age = age
        self.childrenNumber = utils.generateChildrenNumber()
        self.inmunity = 0
        self.married = False
        self.alive = True

        if sex == 'f':
            self.pregnant = False

    def ageInYears(self):
        return self.sex // 48


class Scope:

    def __init__(self, m, f, period, kind, lamb):
        self.turns = utils.generateTimes(kind, lamb, period)
        self.top = m + f
        self.people = dict()
        self.newSingles = []

        for _ in range(m):
            p = Person('m', utils.randint(0, 100)*48)
            self.people[len(self.people) + 1] = p
            if p.age >= 12:
                self.newSingles.append(len(self.people))

        for _ in range(f):
            p = Person('f', utils.randint(0, 100)*48)
            self.people[len(self.people) + 1] = p
            if p.age >= 12:
                self.newSingles.append(len(self.people))

        self.actual_time = 0
        self.period = period
        self.events = []
        self.couples = []
        self.singlesM = []
        self.singlesF = []
        self.totalDeaths = 0
        self.totalBirths = 0

    def simulate(self):
        while True:
            self.deaths = 0
            self.births = 0

            evTime = time.perf_counter()

            #generate deaths events
            for k, p in self.people.items():
                if p.inmunity <= 0:
                    result, t = utils.generateDeath(p.sex, p.age, self.actual_time)
                    if result:
                        self.events.append((t, 'death', k))
                    else:
                        p.inmunity = t * 2

            evTime = time.perf_counter() - evTime
            log.debug(f'Performance of death events: {evTime}', 'benchmark')
            evTime = time.perf_counter()

            #generate breakups
            toRemove = []
            #c = (idx1, idx2)
            for c in self.couples:
                if utils.Bernoulli(0.2):
                    toRemove.append(c)
                    self.people[c[0]].married = False
                    self.people[c[1]].married = False
                    self.events.append((utils.generateBreakup(self.people[c[0]].age), 'solitude', c[0]))
                    self.events.append((utils.generateBreakup(self.people[c[1]].age), 'solitude', c[1]))
            for i in toRemove:
                self.couples.remove(i)
            toRemove.clear()

            evTime = time.perf_counter() - evTime
            log.debug(f'Performance of breakups events: {evTime}', 'benchmark')
            evTime = time.perf_counter()

            #check events
            n = 0
            toAdd = []
            self.events.sort()
            for e in self.events:
                t, event, args = e
                if t <= self.actual_time + self.turns[0]:
                    n += 1
                    if event == 'death':
                        #death = (time, event_type, person_idx)
                        personIdx = args
                        if self.people[personIdx].alive:
                            self.people[personIdx].alive = False
                            self.deaths += 1
                            if self.people[personIdx].married:
                                for c in self.couples:
                                    if c[0] == personIdx or c[1] == personIdx:
                                        toRemove.append(c)
                                        break
                                c = toRemove.pop()
                                self.couples.remove(c)
                                if c[0] == personIdx:
                                    id = c[1]
                                else:
                                    id = c[0]
                                p = self.people[id]
                                p.married = False
                                toAdd.append((utils.generateBreakup(p.age), 'solitude', id))
                    elif event == 'solitude':
                        #solitude = (time, event_type, person_idx)
                        personIdx = args
                        if self.people[personIdx].alive:
                            self.newSingles.append(personIdx)
                    elif event == 'birth':
                        #birth = (time, event_type, ((father_idx, mother_idx), children_number)
                        fathers, cn = args
                        if self.people[fathers[1]].alive:
                            self.people[fathers[1]].pregnant = False
                            for c in range(cn):
                                self.births += 1
                                if utils.Bernoulli(0.5):
                                    self.people[len(self.people) + 1] = Person('f', 0)
                                else:
                                    self.people[len(self.people) + 1] = Person('m', 0)
                            self.people[fathers[0]].childrenNumber -= cn
                            self.people[fathers[1]].childrenNumber -= cn
                else:
                    break
            for i in range(n):
                self.events.pop(0)
            for i in toAdd:
                self.events.append(i)

            evTime = time.perf_counter() - evTime
            log.debug(f'Performance of check events: {evTime}', 'benchmark')
            evTime = time.perf_counter()

            #generate couple wishes
            for id in self.newSingles:
                if self.people[id].age // 48 >= 12 and utils.generateWishCouple(self.people[id].age):
                    toRemove.append(id)
                    if self.people[id].sex == 'm':
                        self.singlesM.append(id)
                    else:
                        self.singlesF.append(id)
            for i in toRemove:
                self.newSingles.remove(i)
            toRemove.clear()

            evTime = time.perf_counter() - evTime
            log.debug(f'Performance of couple wishes events: {evTime}', 'benchmark')
            evTime = time.perf_counter()

            #set couples
            utils.shuffle(self.singlesM)
            utils.shuffle(self.singlesF)

            for m in self.singlesM:
                for w in self.singlesF:
                    if utils.marry(self.people[m].age, self.people[w].age):
                        self.people[m].married = True
                        self.people[w].married = True
                        self.couples.append((m, w))
                        toRemove += [m]
                        self.singlesF.remove(w)
                        break
            for i in toRemove:
                self.singlesM.remove(i)
            toRemove.clear()

            evTime = time.perf_counter() - evTime
            log.debug(f'Performance of set couples events: {evTime}', 'benchmark')
            evTime = time.perf_counter()

            #generate pregnats
            for c in self.couples:
                if not self.people[c[1]].pregnant and self.people[c[0]].childrenNumber > 0 and self.people[c[1]].childrenNumber > 0:
                    while True:
                        cb = utils.generatePregnancy()
                        if self.people[c[0]].childrenNumber >= cb and self.people[c[1]].childrenNumber >= cb:
                            if utils.generateBirth(self.people[c[1]].age):
                                self.people[c[1]].pregnant = True
                                self.events.append((self.actual_time + 36, 'birth', (c, cb)))
                            break

            evTime = time.perf_counter() - evTime
            log.debug(f'Performance of pregnats events: {evTime}', 'benchmark')
            evTime = time.perf_counter()

            #update date
            turn = self.turns.pop(0)
            if turn >= self.period:
                break
            for id, p in self.people.items():
                if p.alive:
                    oldAge = p.age
                    p.age += turn - self.actual_time
                    if p.age >= 6000: 
                        #125 years old !!!
                        self.events.append((turn, 'death', id))
                    if p.age >= 12 * 48 and oldAge < 12 * 48:
                        self.newSingles.append(id)
                    if p.inmunity <= 0:
                        p.inmunity -= turn - self.actual_time
            self.actual_time = turn

            evTime = time.perf_counter() - evTime
            log.debug(f'Performance of update date: {evTime}', 'benchmark')

            self.totalBirths += self.births
            self.totalDeaths += self.deaths
            
            #self.summary()
            log.info(f'Turn passed!, {self.actual_time // 48}, deaths: {self.deaths}, births: {self.births}')
def main(args):
    kind = ''
    lamb = 0.0
    if args.uniform != '':
        kind = args.uniform
        lamb = args.length
    else:
        kind = args.Poisson
        lamb = args.lamb

    s = Scope(args.males, args.females, args.period, kind, lamb)
    s.simulate()
    s.summary()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='People evolution simulator')
    parser.add_argument('-m', '--males', type=int, default=1000, help='number of initial male people')
    parser.add_argument('-f', '--females', type=int, default=1000, help='number of initial female people')
    parser.add_argument('-p', '--period', type=int, default=4800, help='number of weeks of the entire simulation period')
    parser.add_argument('-u', '--uniform', type=str, const='Uniform', nargs='?', help='use an uniform random variable to generate time evolution')
    parser.add_argument('-l', '--length', type=int, default=48, help='limit of the uniform random variable in number of weeks')
    parser.add_argument('-P', '--poisson', type=str, const='Poisson', nargs='?', help='use a poisson random variable to generate time evolution')
    parser.add_argument('-L', '--lamb', type=float, default=0.0265,help='lambda for poisson if poisson mode is specified')
    parser.add_argument('-v', '--level', type=str, default='INFO', help='log level')

    args = parser.parse_args()
    log.setLevel('DEBUG')
    main(args)