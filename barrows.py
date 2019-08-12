import random as r
import time as t
from threading import Thread
from tkinter import *
from tkinter.ttk import *


class GUI:

    def __init__(self):

        self.item_prob = 1 / 17.4
        self.total_number_uniques = 24

        self.root = Tk()
        self.root.title('Progress')

        self.progresslabel = Label(self.root)
        self.progresslabel.pack(pady=(10, 0))

        self.progressbar = Progressbar(self.root, length=200)
        self.progressbar.pack(pady=10, padx=40)

        self.sim_thread = Thread(target=self.run_sim, daemon=True)

    def run(self):

        self.sim_thread.start()
        self.root.mainloop()

    def __open_chest(self, loot):
        diceroll = r.random()

        if diceroll <= self.item_prob:
            item_gained = r.randrange(len(loot))
            loot[item_gained] += 1
            if loot[item_gained] == 1:
                return True

        return False

    @staticmethod
    def __divider(length=38):
        print('-' * length)

    def run_sim(self):
        # Start the timer
        start_time = t.time()

        # Number of characters to simulate
        num_runs = 10000

        # Keeps track of the number of chests per character, and in total, respectively
        chest_counter = 0
        total_chest_counter = 0

        # Keeps track of the total number of unique items received on all characters
        total_number_of_uniques = 0

        # Keeps track of how many of each unique is acquired per character
        unique_item_counts = [0] * self.total_number_uniques

        # Keeps track of how many kc each number of uniques took to get
        unique_kc = [0] * self.total_number_uniques
        total_unique_kc = [0] * self.total_number_uniques

        # On which interval should the program spit out progress notifications.
        # For instance, if percent_interval = 10, program will ping the console
        # every 10%.
        percent_interval = 10

        print(f'Beginning {num_runs} simulations...')
        self.__divider()

        if percent_interval <= 0:
            percent_interval = 100

        for i in range(num_runs):

            if i != 0 and (i % (num_runs * (percent_interval / 100)) == 0):
                print(f'Progress - {i}/{num_runs} ({round(i/num_runs*100)}%) [{round(t.time()-start_time, 2)}s]')

            percent = round(i / num_runs * 100, 2)
            self.progressbar['value'] = percent
            self.progresslabel['text'] = str(round(percent)) + '%'

            current_number_of_uniques = 0

            while True:

                chest_counter += 1
                if self.__open_chest(unique_item_counts):

                    current_number_of_uniques += 1
                    unique_kc[current_number_of_uniques - 1] = chest_counter

                    if current_number_of_uniques == self.total_number_uniques:
                        break

            for j in range(len(unique_kc)):
                total_unique_kc[j] += unique_kc[j]

            total_number_of_uniques += sum(unique_item_counts)
            total_chest_counter += chest_counter
            chest_counter = 0
            unique_item_counts = [0] * self.total_number_uniques
            unique_kc = [0] * self.total_number_uniques

        average_kc = [round(item / num_runs) for item in total_unique_kc]

        # Stop the timer
        end_time = t.time()

        print('Done!')
        self.__divider()

        print()

        print(f'Characters simulated: {num_runs}')
        print(f'Average chests to completion: {round(total_chest_counter/num_runs)}')
        print('Average kc for each number of uniques:')

        self.__divider(34)
        print('|# Uniques | Average KC|    Diff |')
        self.__divider(34)
        for i in range(len(average_kc)):

            if i == 0:
                diff = 'N/A'
            else:
                diff = average_kc[i] - average_kc[i - 1]

            print('|%9d | %-9d | %7s |' % (i + 1, average_kc[i], str(diff)))

        self.__divider(34)

        print(f'Average total number of uniques per character: {round(total_number_of_uniques/num_runs)}')
        print(f'Total number of chests opened: {total_chest_counter:,}')
        print(f'Simulation took {round(end_time-start_time,3)} seconds')
        print(f'Bye!\n')

        self.root.destroy()

if __name__ == "__main__":
    GUI().run()
