from tkinter import Button
from tkinter import NE, N
import tkinter.font as tkfont

from helpermodules.constants import DEF_BUTTON_FUNC, DEF_BUTTON_HEIGHT, DEF_BUTTON_TEXT, DEF_BUTTON_WIDTH
from helpermodules.constants import PADX, PADY

from helpermodules.MyFonts import FONTS

class MyButton(Button):

    def __init__(
        self,
        parent,
        controller,
        text : str = DEF_BUTTON_TEXT,
        command = DEF_BUTTON_FUNC,
        width:int = DEF_BUTTON_HEIGHT,
        font=FONTS['BUTTON_FONT'],
        x = 0,
        y = 0,
        relx=0,
        rely=0,
        anchor=NE,
        grid = None,
        pady=PADY,
        padx=PADX,
        sticky=N,
        state="normal"
    ):
        Button.__init__(
            self,
            parent,
            text=text,
            command=command,
            font=tkfont.Font(**font),
            state=state
        )
        if not grid:
            self.place(rely=rely, relx=relx, x=x, y=y, anchor=anchor)
        else:
            row, col = grid
            self.grid(row=row, column=col, pady=pady, padx=padx, sticky=sticky)
