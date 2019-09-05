import random as r
import time as t
from GUI import Progress_GUI

# armor = 1/127
# hilt = 1/508

def kill(loot):

    diceroll = r.randint(0, 507)

    if diceroll <= 3:
        loot[diceroll] += 1

        if loot[diceroll] == 1:
            return True

    return False


def armadyl(progresslabel=None, progressbar=None, args=None):

    num_runs = 100000
    total_kc = 0

    start_time = t.time()

    for i in range(num_runs):

        percent = i/num_runs*100

        if progressbar is not None and progresslabel is not None:

            progresslabel['text'] = str(round(percent)) + '%'
            progressbar['value'] = percent

        num_uniques = 0
        killcount = 0
        loot = [0] * 4

        while True:

            killcount += 1
            if kill(loot):

                num_uniques += 1

                if num_uniques == 4:
                    break

        total_kc += killcount

    end_time = t.time()

    average_kc = total_kc/num_runs

    print(f'Average kc:{average_kc} ({round(end_time-start_time, 2)}s)')


Progress_GUI(armadyl, "Armadyl")
