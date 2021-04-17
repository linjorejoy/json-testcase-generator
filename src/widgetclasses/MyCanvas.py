from tkinter import Canvas
from tkinter import LEFT, BOTH


class MyCanvas(Canvas):

    def __init__(
        self,
        parent,
        controller,
        side:str=LEFT,
        fill:str=BOTH,
        expand = 1,
        yscrollcommand = None,
        xscrollcommand = None
    ):
        Canvas.__init__(self, parent)
        self.pack(side=side, fill=fill, expand=expand)

        if yscrollcommand:
            self.config(yscrollcommand=yscrollcommand)

        if xscrollcommand:
            self.config(xscrollcommand=xscrollcommand)
