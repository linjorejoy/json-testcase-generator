from tkinter import Text
from tkinter import WORD, NSEW, TOP, END, BOTH
import tkinter.font as tkfont

from helpermodules.constants import DEF_TEXT_TEXT
from helpermodules.MyFonts import FONTS

class MyText(Text):

    def __init__(
        self,
        parent,
        controller,
        width:int,
        height:int,
        wrap:str = WORD,
        text:str = DEF_TEXT_TEXT,
        font = FONTS['DEFAULT_TEXT_FONT'],
        sticky:str=NSEW
    ):
        Text.__init__(self, parent, wrap=wrap, font=tkfont.Font(**font))
        # print(**font)

        self.insert(END, text)
        self.pack(side=TOP, fill=BOTH, expand="yes")
