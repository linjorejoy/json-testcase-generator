from tkinter import Scrollbar
from tkinter import RIGHT, Y
from tkinter.font import Font

class MyScrollBar(Scrollbar):

    def __init__(
        self,
        parent,
        controller,
        command = None,
        orient:str="vertical",
        side:str=RIGHT, fill:str=Y
    ):
        Scrollbar.__init__(self, parent, orient=orient)
        self.pack(side=side, fill=fill)
        if command:
            self.config(command=command)
