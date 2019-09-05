import random as r
import time as t
import GUI
import Cache
from tkinter import *
from tkinter.ttk import *

ITEM_PROB = 1 / 17.4
TOTAL_NUMBER_UNIQUES = 24

unique_ids = [4732, 4734, 4736, 4738,  # Karil
              4708, 4710, 4712, 4714,  # Ahrim
              4745, 4747, 4749, 4751,  # Torag
              4753, 4755, 4757, 4759,  # Verac
              4726, 4728, 4730, 4732,  # Guthan
              4716, 4718, 4720, 4722]  # Dharok


unique_info = []
for item_id in unique_ids:
    item_info = Cache.get_cached_item(item_id)
    item_dict = {}
    item_dict.setdefault('name', item_info['name'])
    item_dict.setdefault('price', Cache.convert_to_double(item_info['current']['price']))
    unique_info.append(item_dict)

print(unique_info)


def open_chest(loot):
    diceroll = r.random()

    if diceroll <= ITEM_PROB:
        item_gained = r.randrange(len(loot))
        loot[item_gained] += 1
        if loot[item_gained] == 1:
            return True

    return False


def divider(length=38):
    print('-' * length)


def barrows(progresslabel, progressbar, extra_args=None):
    # Start the timer
    start_time = t.time()

    # Number of characters to simulate
    num_runs = extra_args['num_runs'] if extra_args is not None else 10000

    # Keeps track of the number of chests per character, and in total, respectively
    chest_counter = 0
    total_chest_counter = 0

    # Keeps track of the total number of unique items received on all characters
    total_number_of_uniques = 0

    # Keeps track of how many of each unique is acquired per character
    unique_item_counts = [0] * TOTAL_NUMBER_UNIQUES

    # Keeps track of how many kc each number of uniques took to get
    unique_kc = [0] * TOTAL_NUMBER_UNIQUES
    total_unique_kc = [0] * TOTAL_NUMBER_UNIQUES

    total_item_drop_count = [0] * 24

    # On which interval should the program spit out progress notifications.
    # For instance, if percent_interval = 10, program will ping the console
    # every 10%.
    percent_interval = 10

    print(f'Beginning {num_runs} simulations...')
    divider()

    if percent_interval <= 0:
        percent_interval = 100

    for i in range(num_runs):

        if i != 0 and (i % (num_runs * (percent_interval / 100)) == 0):
            print(f'Progress - {i}/{num_runs} ({round(i/num_runs*100)}%) [{round(t.time()-start_time, 2)}s]')

        percent = round(i / num_runs * 100, 2)
        progressbar['value'] = percent
        progresslabel['text'] = str(round(percent)) + '%'

        current_number_of_uniques = 0

        while True:

            chest_counter += 1
            if open_chest(unique_item_counts):

                current_number_of_uniques += 1
                unique_kc[current_number_of_uniques - 1] = chest_counter

                if current_number_of_uniques == TOTAL_NUMBER_UNIQUES:
                    break

        for j in range(len(unique_kc)):
            total_unique_kc[j] += unique_kc[j]

        for j in range(len(unique_item_counts)):
            total_item_drop_count[j] += unique_item_counts[j]

        total_number_of_uniques += sum(unique_item_counts)
        total_chest_counter += chest_counter
        chest_counter = 0
        unique_item_counts = [0] * TOTAL_NUMBER_UNIQUES
        unique_kc = [0] * TOTAL_NUMBER_UNIQUES

    average_kc = [round(item / num_runs) for item in total_unique_kc]

    # Stop the timer
    end_time = t.time()

    average_item_drop_count = [item_count/num_runs for item_count in total_item_drop_count]
    profit_per_item = [0] * TOTAL_NUMBER_UNIQUES

    for i in range(TOTAL_NUMBER_UNIQUES):
        profit_per_item[i] = unique_info[i]['price'] * average_item_drop_count[i]

    print('Done!')
    divider()

    print()

    print(f'Characters simulated: {num_runs}')
    print(f'Average chests to completion: {round(total_chest_counter/num_runs)}')
    print('Average kc for each number of uniques:')

    divider(34)
    print('|# Uniques | Average KC|    Diff |')
    divider(34)
    for i in range(len(average_kc)):

        if i == 0:
            diff = 'N/A'
        else:
            diff = average_kc[i] - average_kc[i - 1]

        print('|%9d | %-9d | %7s |' % (i + 1, average_kc[i], str(diff)))

    divider(34)

    print(f'Average total number of uniques per character: {round(total_number_of_uniques/num_runs)}')
    print(f'Average profit: {round(sum(profit_per_item), 2):,}')
    print(f'Total number of chests opened: {total_chest_counter:,}')
    print(f'Simulation took {round(end_time-start_time,3)} seconds')
    print(f'Bye!\n')


class ResultsGUI:

    # The format of results should be as follows:
    # The first element is a list of tuples of the following format:
    #  (item name, item price, number dropped, total profit)
    # The rest of the elements are tuples as such:
    #  (message, value)

    def __init__(self, results, title='Results'):

        self.root = root = Tk()
        self.root.title(title)

    def run(self):

        self.root.mainloop()


if __name__ == "__main__":

    args = {'num_runs': 1000, 'results': []}
    progress = GUI.ProgressGUI(barrows, title=f"Barrows ({args['num_runs']:,})", extra_args=args)
    progress.run()
    # resultsGUI = ResultsGUI(args['results'])
    # resultsGUI.run()
