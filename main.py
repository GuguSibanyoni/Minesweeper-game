from tkinter import *
import random
import sys

class Game_Grid(Frame):
    def __init__(self, master, height, width,mines_count, player):
        Frame.__init__(self, master)
        self.grid(row=)
        self.master = master
        if sys.platform == 'win32':
            self.platform = 'windows'
        else:
            self.platform = 'macos'
            self.height
