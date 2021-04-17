from tkinter import OptionMenu
from tkinter import StringVar

from helpermodules.constants import PADX, PADY



class MyOptionMenu(OptionMenu):

    def __init__(
        self,
        parent,
        controller,
        variable:StringVar,
        options:list=["No","Options","Given"],
        x = 0,
        y = 0,
        relx=0,
        rely=0,
        grid = None,
        pady=PADY,
        padx=PADX
    ):
        OptionMenu.__init__(self, parent, variable, *options)
        if grid:
            row, col = grid
            self.grid(row=row, column=col, padx=padx, pady=pady)
        else:
            self.place(rely=rely, relx=relx, x=x, y=y, anchor=anchor)
