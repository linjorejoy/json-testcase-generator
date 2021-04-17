from tkinter import Label
from tkinter import NE
import tkinter.font as tkfont

from helpermodules.constants import DEF_LABEL_TEXT, PADX, PADY
from helpermodules.MyFonts import FONTS



class MyLabel(Label):

    def __init__(
        self,
        parent,
        controller,
        text:str=DEF_LABEL_TEXT,
        font = None,
        x:int = 0,
        y:int = 0,
        relx:int = 0,
        rely:int = 0,
        anchor=NE,
        grid=None,
        pady=PADY,
        padx=PADX
    ):
        Label.__init__(self, parent, text=text, font=tkfont.Font(**FONTS['LABEL_FONT']))

        if not grid:
            self.place(x=x, y=y, relx=relx, rely=rely, anchor=anchor)
        else:
            row, col = grid
            self.grid(row=row, column=col, pady=pady, padx=padx)
