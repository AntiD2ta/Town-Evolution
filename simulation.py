import utils

log = utils.LoggerFactory(name='Simulator')


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
        self.turns = utils.generateTimes(kind, lamb)
        self.top = m + f
        self.people = dict()
        self.newSingles = []

        for _ in range(m):
            p = Person('m', utils.randint(0, 100))
            self.people[len(self.people) + 1] = p
            if p.age >= 12:
                self.newSingles.append(len(self.people))

        for _ in range(f):
            p = Person('f', utils.randint(0, 100))
            self.people[len(self.people) + 1] = p
            if p.age >= 12:
                self.newSingles.append(len(self.people))

        self.actual_time = 0
        self.period = period
        self.events = set()
        self.inmunities = set()
        self.couples = []
        self.singlesM = []
        self.singlesF = []

    def simulate(self):
        while True:
            #generate deaths events
            for k, p in self.people.items():
                if not p.inmunity:
                    result, t = utils.generateDeath(p.sex, p.age, self.actual_time)
                    if result:
                        self.events.add((t, 'death', k))
                    else:
                        p.inmunity = t
                        self.inmunities.add(k)

            #generate breakups
            toRemove = []
            #c = (idx1, idx2)
            for i, c in enumerate(self.couples):
                if utils.Bernoulli(0.2):
                    toRemove.append(i)
                    self.people[c[0]].married = False
                    self.people[c[1]].married = False
                    self.events.add((utils.generateBreakup(self.people[c[0]].age), 'solitude', c[0]))
                    self.events.add((utils.generateBreakup(self.people[c[1]].age), 'solitude', c[1]))
            for i in toRemove:
                self.couples.pop(i)
            toRemove.clear()

            #check events
            for e in self.events:
                t, event, personIdx = e
                if t <= self.actual_time + self.turns[0]:
                    if event == 'death':
                        #death = (time, event_type, person_idx)
                        self.people[personIdx].alive = False
                        if self.people[personIdx].married:
                            for i, c in enumerate(self.couples):
                                if c[0] == personIdx or c[1] == personIdx:
                                    toRemove.append(c)
                                    break
                            c = self.couples.pop(toRemove.pop())
                            if c[0] == personIdx:
                                id = c[1]
                            else:
                                id = c[0]
                            p = self.people[id]
                            p.married = False
                            self.events.add((utils.generateBreakup(p.age), 'solitude', id))
                    elif event == 'solitude':
                        #solitude = (time, event_type, person_idx)
                        pass
                    elif event == 'birth':
                        #birth = (time, event_type, ((father_idx, mother_idx), children_number)
                        pass


            #generate couple wishes
            for i, id in enumerate(self.newSingles):
                if utils.generateWishCouple(self.people[id].age):
                    toRemove.append(id)
                    if self.people[id].sex == 'm':
                        self.singlesM.append(id)
                    else:
                        self.singlesF.append(id)
            for i in toRemove:
                self.newSingles.pop(i)
            toRemove.clear()

            #set couples
            utils.shuffle(self.singlesM)
            utils.shuffle(self.singlesF)

            for m in self.singlesM:
                for w in self.singlesF:
                    if utils.marry(self.people[m].age, self.people[w].age):
                        self.people[m].married = True
                        self.people[w].married = True
                        self.couples.append((m, w))
                        toRemove += [m, w]
                        break
                if len(toRemove):
                    self.singlesF.remove(toRemove[-1])
            for i in toRemove:
                self.singlesM.remove(i)
            toRemove.clear()

            #generate pregnats
            for c in self.couples:
                if self.people[c[0]].childrenNumber > 0 and self.people[c[1]].childrenNumber > 0:
                    while True:
                        cb = utils.generatePregnancy()
                        if self.people[c[0]].childrenNumber > cb and self.people[c[1]].childrenNumber > cb and utils.generateBirth(self.people[c[1]].age):
                            self.events.add((self.actual_time + 36, 'birth', (c, cb)))
                            break

            #update date
            turn = self.turns.pop()
            if turn >= self.period:
                break
            for id, p in self.people.items():
                if p.alive:
                    oldAge = p.age
                    p.age += turn - self.actual_time
                    if p.age >= 12 * 48 and oldAge < 12 * 48:
                        self.newSingles.append(id)
            self.actual_time = turn


def main(args):
    pass

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='People evolution simulator')
    parser.add_argument('-m', '--males', type=int, default=800000, help='number of initial male people')
    parser.add_argument('-f', '--female', type=int, default=1000000, help='number of initial female people')
    parser.add_argument('-p', '--period', type=int, default=4800, help='number of weeks of the entire simulation period')
    parser.add_argument('-u', '--uniform', type=str, const='Uniform', help='use an uniform random variable to generate time evolution')
    parser.add_argument('-p', '--poisson', type=str, const='Poisson', help='use a poisson random variable to generate time evolution')
    parser.add_argument('-l', '--lambda', type=float, help='lambda for poisson if poisson mode is specifided')

    args = parser.parse_args()

    main(args)