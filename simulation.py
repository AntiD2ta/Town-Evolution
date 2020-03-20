import utils

log = utils.LoggerFactory(name="Simulator")


class Person:

    def __init__(self, sex, age):
        self.sex = sex
        self.age = age
        self.childrenNumber = utils.generateChildrenNumber()
        self.inmunity = 0

        if sex == 'f':
            self.pregnant = False

    def ageInYears(self):
        return self.sex // 48


class Scope:

    def __init__(self, m, f, period, kind, lamb):
        self.turns = utils.generateTimes(kind, lamb)
        self.top = m + f
        self.people = dict()

        for _ in range(m):
            self.people[len(self.people) + 1] = Person("male", utils.randint(0, 100))
        for _ in range(f):
            self.people[len(self.people) + 1] = Person("female", utils.randint(0, 100))

        self.actual_time = 0
        self.period = period
        self.events = set()
        self.inmunities = set()

    def simulate(self):
        #generate deaths events
        for k, p in self.people.items():
            if not p.inmunity:
                result, t = utils.generateDeath(p.sex, p.age, self.actual_time)
                if result:
                    self.events.add((t, "death"))
                else:
                    p.inmunity = t
                    self.inmunities.add(k)

        #generate breakups

        #check events

        #generate couple wishes

        #set couples

        #generate pregnats

        #update date

def main(args):
    pass

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='People evolution simulator')
    parser.add_argument('-m', '--males', type=int, default=800000, help='number of initial male people')
    parser.add_argument('-f', '--female', type=int, default=1000000, help='number of initial female people')
    parser.add_argument('-p', '--period', type=int, default=4800, help='number of weeks of the entire simulation period')

    args = parser.parse_args()

    main(args)