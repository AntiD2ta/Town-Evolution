import utils

class Person:

    def __init__(self, sex, age):
        self.sex = sex
        self.age = age
        self.children_number = utils.generateChildrenNumber()

        if sex == 'f':
            self.pregnant = False

    def age_in_years(self):
        return self.sex // 48


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