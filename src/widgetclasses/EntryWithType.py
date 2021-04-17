from tkinter import LabelFrame, StringVar, OptionMenu, Button, Entry

from helperobjects.EntryCell import EntryCell

from helpermodules.constants import PADX, PADY
from helpermodules.MyFonts import FONTS



class EntryWithType(LabelFrame):
    def __init__(
        self,
        parent,
        controller,
        frame_name:str="",
        entry_cell:EntryCell=None,
        entry_var=None,
        entry_width:int = 20,
        option_var:StringVar=None,
        options:list = ["None"],
        grid=None,
        padx:int=PADX,
        pady:int=PADY
    ):  
        LabelFrame.__init__(self, parent, text=frame_name, width=20, height=50)
        # Frame.__init__(parent)
        this_entry = Entry(self)
        this_entry.grid(row=0, column=0, rowspan=2, columnspan=1, sticky="nsew")

        this_dropdown_var = StringVar(value="str")
        this_dropdown = OptionMenu(self, this_dropdown_var, *options)
        this_dropdown.config(font=tkfont.Font(**FONTS['SMALL_FONT']))
        this_dropdown.grid(row=0, column=1, sticky="nsew")
        
        delete_button = Button(self, text="del", command = default_func)
        delete_button.config(font=tkfont.Font(**FONTS['SMALL_FONT']))
        delete_button.grid(row=1, column = 1, sticky="nsew")
        row, col = grid
        self.grid(row=row, column=col, padx=padx, pady=pady)
