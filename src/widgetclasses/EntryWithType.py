from tkinter import LabelFrame, StringVar, OptionMenu, Button, Entry, EW, END
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
        entry_def_value:str=None,
        options:list = ["None"],
        add_del_button=True,
        delete_command=default_func,
        show_add_cell_button=False,
        add_cell_command = default_func,
        grid=None,
        padx:int=PADX,
        pady:int=PADY
    ):  
        LabelFrame.__init__(self, parent, text=frame_name, width=20, height=50)

        self.this_dropdown = OptionMenu(self, entry_cell.option_value, *options)
        self.this_dropdown.config(font=tkfont.Font(**FONTS['SMALL_FONT']))
        self.this_dropdown.grid(row=0, column=0, sticky="nsew")
        
        self.this_entry = Entry(self)
        if entry_def_value:
            self.this_entry.insert(END, entry_def_value)
            
        self.this_entry.grid(row=0, column=1, sticky="nsew")
        entry_cell.entry = self.this_entry

        if add_del_button:
        
            self.delete_button = Button(self, text="X", command = delete_command)
            self.delete_button.config(font=tkfont.Font(**FONTS['SMALL_FONT_2']))
            self.delete_button.grid(row=0, column = 2, sticky="nsew")
        
        if show_add_cell_button:

            self.add_cell_button = Button(self, text="+", command = add_cell_command)
            self.add_cell_button.config(font=tkfont.Font(**FONTS['SMALL_FONT_2']))
            self.add_cell_button.grid(row=0, column = 3, sticky="nsew")

        row, col = grid
        self.grid(row=row, column=col, padx=padx, pady=pady, sticky=EW)
    
    def destroy(self):
        return super().destroy()