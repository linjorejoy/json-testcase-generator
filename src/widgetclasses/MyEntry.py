from tkinter import Entry
from tkinter import NW


from helpermodules.constants import PADX, PADY


class MyEntry(Entry):

    def __init__(
        self,
        parent,
        controller,
        x = 0,
        y = 0,
        relx=0,
        rely=0,
        anchor=NW,
        grid = None,
        pady=PADY,
        padx=PADX,
        sticky=None

    ):
        Entry.__init__(self, parent)
        if not grid:
            self.place(rely=rely, relx=relx, x=x, y=y, anchor=anchor)
        else:
            row, col = grid
            self.grid(row=row, column=col, pady=pady, padx=padx, sticky=sticky)
