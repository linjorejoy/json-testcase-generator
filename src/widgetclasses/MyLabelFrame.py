from tkinter import LabelFrame

from helpermodules.constants import DEF_LABELFRAME_TEXT, DEF_LABELFRAME_HEIGHT, DEF_LABELFRAME_EXPAND, DEF_LABELFRAME_FILL

class MyLabelFrame(LabelFrame):
    def __init__(
        self,
        parent,
        controller,
        text:str=DEF_LABELFRAME_TEXT,
        height:str=DEF_LABELFRAME_HEIGHT,
        expand:str=DEF_LABELFRAME_EXPAND
    ):
        LabelFrame.__init__(self, parent, text=text, height=height)

        self.pack(fill=DEF_LABELFRAME_FILL, expand=expand)
