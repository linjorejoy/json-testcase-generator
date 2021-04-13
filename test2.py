from tkinter import Tk, Frame, filedialog, LabelFrame, Scrollbar, OptionMenu, Checkbutton, Canvas
from tkinter import Text, Button, Label, Entry
from tkinter import IntVar, StringVar
from tkinter import ttk
from tkinter.ttk import Combobox, Treeview, Progressbar
from tkinter import RIGHT, LEFT, END, BOTH, TOP, SE, W, NSEW, BOTTOM, HORIZONTAL, VERTICAL
from tkinter import X, Y, N, WORD
import json
import os
from functools import partial

from helperobjects.EntryCellCollection import EntryCellCollection
from helperobjects.EntryCellColumn import EntryCellColumn
from helperobjects.EntryCell import EntryCell
from helperobjects.OutputFiles import OutputFiles
from helperobjects.OutputJsonFile import OutputJsonFile

import helpermodules.ProcessData as ProcessData
import helpermodules.GetAllCombinations as GetAllCombinations
import helpermodules.FileNameGenerator as FileNameGenerator
import helpermodules.GenerateFile as GenerateFile

# 

CURRENT_VERSION = "V0.0.7"
ICON = "src/resources/favicon-32x32.ico"

FONTS = {
    "LARGE_FONT": ("bold", 12),
    "BUTTON_FONT": ("bold", 10),
    "LABEL_FONT": ("bold", 10)
}

def default_func():
    print("Assign command to this button")

def print_smtg(string):
    print(string)


class JsonTestCaseTracker(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        
        

        # For Storing Frames
        self.frames = {}


        # Global Variables
        self.TEMPLATE_JSON_FILE = ""
        self.json_data = {}
        self.JSON_STR = ""
        self.JSON_STR_TO_PRINT = ""
        self.VARIABLES_PRESENT = []
        self.entry_cell_collection = None
        self.output_files = OutputFiles()
        self.output_location = ""
        self.reference_arr_for_name_gen = []



        # Setting UI 
        Tk.iconbitmap(self, default=ICON)
        Tk.wm_title(self, f"JSON Test Case Tracker {CURRENT_VERSION}")



        # Setting Size of UI
        Tk.geometry(self, self.get_screen_dimentions(0.75))
        

        # Global Container
        global_container = Frame(self)
        global_container.pack(side=TOP, fill=BOTH, expand=True)

        global_container.grid_rowconfigure(0, weight=1)
        global_container.columnconfigure(0, weight=1)


        FRAMES = [StartPage, PageOne, PageTwo, UploadPage]

        for FRAME in FRAMES:
            frame = FRAME(global_container, self)
            self.frames[FRAME] = frame
            frame.grid(row=0, column=0, sticky=NSEW)


        self.show_frame(UploadPage)


    def show_frame(self, controller):

        frame = self.frames[controller]
        frame.tkraise()


    def get_screen_dimentions(self, ratio:float = 0.8):
        
        ScreenSizeX = self.winfo_screenwidth()
        ScreenSizeY = self.winfo_screenheight()
        ScreenRatio = ratio
        FrameSizeX  = int(ScreenSizeX * ScreenRatio)
        FrameSizeY  = int(ScreenSizeY * ScreenRatio)
        FramePosX   = int((ScreenSizeX - FrameSizeX)/2)
        FramePosY   = int((ScreenSizeY - FrameSizeY)/2)
        
        return f"{FrameSizeX}x{FrameSizeY}+{FramePosX}+{FramePosY}"


class StartPage(Frame):

    def __init__(self, parent, controller:JsonTestCaseTracker):
        Frame.__init__(self, parent)

        test_label = Label(self, text="Page 0 : Hello World", font = FONTS["LARGE_FONT"])
        test_label.pack(padx=10, pady=10)

        button1 = Button(
            self,
            text="Goto Page 1",
            command=lambda:controller.show_frame(PageOne)
        )
        button1.pack(pady=10, padx=10)


class PageOne(Frame):

    def __init__(self, parent, controller: JsonTestCaseTracker):
        Frame.__init__(self, parent)

        test_label = Label(self, text="Page 1", font = FONTS["LARGE_FONT"])
        test_label.pack(padx=10, pady=10)

        button1 = Button(
            self,
            text="Goto Page 2",
            command=lambda:controller.show_frame(PageTwo)
        )
        button1.pack(pady=10, padx=10)


class PageTwo(Frame):

    def __init__(self, parent, controller: JsonTestCaseTracker):
        Frame.__init__(self, parent)

        test_label = Label(self, text="Page 2", font = FONTS["LARGE_FONT"])
        test_label.pack(padx=10, pady=10)

        button1 = Button(
            self,
            text="Goto Page 0",
            command=lambda:controller.show_frame(StartPage)
        )
        button1.pack(pady=10, padx=10)


class UploadPage(Frame):

    def __init__(self, parent, controller: JsonTestCaseTracker):

        Frame.__init__(self, parent)

        head_wrapper = Wrapper(self, controller, text="Head", expand=N)
        
        upload_label = MyLabel(
            head_wrapper, controller,
            text="Please Upload the JSON Template File : ",
            font=FONTS['LABEL_FONT'],
            x = 250, y = 0
        )

        upload_button = MyButton(
            head_wrapper, controller,
            text="Select File",
            width=20,
            x = 500,
            y = 0
        )
        
        body_wrapper = Wrapper(self, controller, text="Body")
        footer_wrapper = Wrapper(self, controller, text="Footer", expand=N)

        next_button = Button(
            self,
            text="Goto Page 0",
            command=lambda:controller.show_frame(StartPage)
        )
        next_button.pack(pady=10, padx=10)


class Wrapper(LabelFrame):
    def __init__(
        self,
        parent,
        controller : JsonTestCaseTracker,
        text:str="Wrapper",
        height:str="50",
        expand:str="yes"
    ):
        LabelFrame.__init__(self, parent, text=text, height=height)

        self.pack(fill="both", expand=expand)


class MyLabel(Label):

    def __init__(
        self,
        parent,
        controller :JsonTestCaseTracker,
        text:str="Enter Something",
        font = FONTS["LABEL_FONT"],
        x:int = None,
        y:int = None
    ):
        Label.__init__(self, parent, text=text, font=font)
        if x is not None and y is not None:
            self.place(x=x, y=y)


class MyButton(ttk.Button):

    def __init__(
        self,
        parent,
        controller : JsonTestCaseTracker,
        text : str = "Button",
        command = default_func,
        width:int = 25,
        x = None,
        y = None
    ):
        ttk.Button.__init__(self, parent, text=text, command=command, width= width)

        if x is not None and y is not None:
            self.place(x=x, y=y)


class EntryWithType(Entry, OptionMenu):
    def __init__(
        self, parent,
        controller,
        entry_var,
        entry_width:int = 20,
        option_var=None,
        options:list = ["None"]
    ):
        pass
    pass


app = JsonTestCaseTracker()
app.mainloop()
