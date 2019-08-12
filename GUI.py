from tkinter import *
from tkinter.ttk import *
from threading import Thread


class GUI:

    def __init__(self, custom_func, title="Progress", extra_args=None):

        self.item_prob = 1 / 17.4
        self.total_number_uniques = 24

        self.root = Tk()
        self.root.title(title)

        self.progresslabel = Label(self.root)
        self.progresslabel.pack(pady=(10, 0))

        self.progressbar = Progressbar(self.root, length=200)
        self.progressbar.pack(pady=10, padx=40)

        self.thread = Thread(target=self.__run_func, args=(custom_func, extra_args), daemon=True)

    def run(self):

        self.thread.start()
        self.root.mainloop()

    def __run_func(self, func, extra_args):

        func(self.progresslabel, self.progressbar, extra_args)
        self.root.destroy()
