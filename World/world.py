from tkinter import *
from tkinter import messagebox
from Bot import Bot, Background
from Structures import Coordinates, Storage, Genome
from threading import Thread
from time import sleep


class World:
    def __init__(self):
        self.main_form = Tk()
        self.main_form.geometry('1000x1000')
        self.main_form.title("AI based on a genetic algorithm (developed by Duuuda)")
        self.main_form['bg'] = "#aaaaaa"
        self.main_form.resizable(width=FALSE, height=FALSE)
        self.__center_screen(self.main_form)
        self.main_form.protocol("WM_DELETE_WINDOW", self.__exit)
        self.bitmap = Canvas(self.main_form, width=1000, height=1000, bg='#ffffff')
        self.bitmap.pack()
        Background(self.bitmap)
        self.storage = Storage()

        bot_1 = Bot(Coordinates(50, 50), self.bitmap, Genome(), self.storage)
        bot_2 = Bot(Coordinates(49, 50), self.bitmap, Genome(color='#ff0000'), self.storage)
        bot_3 = Bot(Coordinates(51, 50), self.bitmap, Genome(color='#ff0000'), self.storage)
        bot_4 = Bot(Coordinates(50, 49), self.bitmap, Genome(), self.storage)
        bot_5 = Bot(Coordinates(50, 48), self.bitmap, Genome(), self.storage)
        bot_6 = Bot(Coordinates(50, 47), self.bitmap, Genome(color='#ff0000'), self.storage)

        self.storage.add_item(bot_1)
        self.storage.add_item(bot_2)
        self.storage.add_item(bot_3)
        self.storage.add_item(bot_4)
        self.storage.add_item(bot_5)
        self.storage.add_item(bot_6)

        answer = messagebox.askyesno(title='Launch of evolution', message='Are you ready to evolve?')
        if not answer:
            raise SystemExit

        thread = Thread(target=self.evolve, args=(), daemon=True)
        thread.start()

        self.main_form.mainloop()

    @staticmethod
    def __center_screen(form):
        form.update_idletasks()
        s = form.wm_geometry()
        s = s[0: s.index('+')].split('x')
        s[0] = (form.winfo_screenwidth() - int(s[0])) // 2
        s[1] = 0
        form.geometry(f'+{s[0]}+{s[1]}')

    @staticmethod
    def __exit():
        answer = messagebox.askyesno(title='Exit', message='Are you sure you want to go out and kill all the bots?')
        if answer:
            raise SystemExit

    def evolve(self):
        while True:
            for key in self.storage.alive.copy().keys():
                bot = self.storage.alive.get(key)
                if bot is not None:
                    bot.evolve()
                    sleep(0.01)
