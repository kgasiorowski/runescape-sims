import random as r
from pprint import pprint


def addValueToAverage(currentAverage, newValue, numValues):
    return currentAverage + ((newValue - currentAverage) / numValues)


def complete(drops):
    for drop in drops:
        if drop == 0:
            return False
    return True


def simulateSingleAccount():
    drops = [0] * 4
    killcount = 0

    while not complete(drops):
        killcount += 1
        if r.random() < 1 / 128:
            drops[r.randint(0, len(drops) - 1)] += 1

    return {'kc': killcount, 'drops': drops}


def simulateAccounts(numAccounts):
    results_list = []

    print("Simulating...")
    for i in range(numAccounts):
        results_list.append(simulateSingleAccount())

    min = {'kc': float("inf"), 'drops': [0]*4}
    max = {'kc': float("-inf"), 'drops': [0]*4}
    avg = {}

    print("Calculating...")
    for i in range(len(results_list)):
        result = results_list[i]

        if result['kc'] < min['kc']:
            min = result
        if result['kc'] > max['kc']:
            max = result

        if i+1 == 1:
            avg = result
            del(avg['drops'])
        else:
            avg['kc'] = addValueToAverage(avg['kc'], result['kc'], i+1)

    print("Sorting...")
    median = sorted(results_list, key=lambda x: x['kc'])[numAccounts//2]
    return {'min': min, 'max': max, 'avg': avg, 'median': median}


if __name__ == "__main__":

    print("1: Prim\n2: Pegs\n3: Eternal\n4: Smouldering")
    pprint(simulateAccounts(10000))
