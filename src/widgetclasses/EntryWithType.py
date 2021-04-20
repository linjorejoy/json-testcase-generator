from tkinter import LabelFrame, StringVar, OptionMenu, Button, Entry
import tkinter.font as tkfont

from helperobjects.EntryCell import EntryCell

from helpermodules.constants import PADX, PADY, default_func
from helpermodules.MyFonts import FONTS



class EntryWithType(LabelFrame):
    def __init__(
        self,
        parent,
        controller,
        frame_name:str="",
        entry_cell:EntryCell=None,
        options:list = ["None"],
        delete_command=default_func,
        grid=None,
        padx:int=PADX,
        pady:int=PADY
    ):  
        LabelFrame.__init__(self, parent, text=frame_name, width=20, height=50)
        # Frame.__init__(parent)
        this_entry = Entry(self)
        this_entry.grid(row=0, column=1, sticky="nsew")
        entry_cell.entry = this_entry

        # option_var = StringVar(value="str")
        this_dropdown = OptionMenu(self, entry_cell.option_value, *options)
        this_dropdown.config(font=tkfont.Font(**FONTS['SMALL_FONT']))
        this_dropdown.grid(row=0, column=0, sticky="nsew")
        
        delete_button = Button(self, text="X", command = self.destroy)
        delete_button.config(font=tkfont.Font(**FONTS['SMALL_FONT']))
        delete_button.grid(row=0, column = 2, sticky="nsew")
        row, col = grid
        self.grid(row=row, column=col, padx=padx, pady=pady)
    
    def destroy(self):
        return super().destroy()