from tkinter import Tk, Frame, filedialog, LabelFrame, Scrollbar, OptionMenu, Checkbutton, Canvas
from tkinter import Text, Button, Label, Entry
from tkinter import IntVar, StringVar
from tkinter import ttk
import tkinter.font as tkfont
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

from helpermodules.MyFonts import FONTS

from helpermodules.constants import SCREEN_RATIO, CURRENT_VERSION, ICON
from helpermodules.constants import ACCEPTABLE_FILE_TYPES
from helpermodules.constants import DEF_BUTTON_TEXT, DEF_BUTTON_FUNC, DEF_BUTTON_WIDTH
from helpermodules.constants import DEF_LABELFRAME_EXPAND, DEF_LABELFRAME_HEIGHT, DEF_LABELFRAME_TEXT, DEF_LABELFRAME_FILL
from helpermodules.constants import DEF_LABEL_TEXT
from helpermodules.constants import DEF_TEXT_TEXT
from helpermodules.constants import JSON_PREVIEW_INDENT
from helpermodules.constants import default_func



class JsonTestCaseTracker(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.FONTS = FONTS
        

        # For Storing Frames
        self.frames = {}


        # Global Variables
        self.TEMPLATE_JSON_FILE = ""
        self.json_data = {}
        self.JSON_STR = "{None}"
        self.JSON_STR_TO_PRINT = f"{None}"
        self.VARIABLES_PRESENT = []
        self.entry_cell_collection = EntryCellCollection()
        self.output_files = OutputFiles()
        self.output_location = ""
        self.reference_arr_for_name_gen = []
        self.current_dir = os.curdir



        # Setting UI 
        Tk.iconbitmap(self, default=ICON)
        Tk.wm_title(self, f"JSON Test Case Tracker {CURRENT_VERSION}")



        # Setting Size of UI
        Tk.geometry(self, self.get_screen_dimentions(SCREEN_RATIO))
        

        # Global Container
        global_container = Frame(self)
        global_container.pack(side=TOP, fill=BOTH, expand=True)

        global_container.grid_rowconfigure(0, weight=1)
        global_container.columnconfigure(0, weight=1)


        FRAMES = [UploadPage, ProcessVariables]

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



class UploadPage(Frame):

    def __init__(self, parent, controller: JsonTestCaseTracker):

        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.indent = JSON_PREVIEW_INDENT
        self.file_name_label = None
        self.json_preview_text = None

        head_wrapper = MyLabelFrame(self, controller, height="100", text="Head", expand=N)
        
        upload_label = MyLabel(
            head_wrapper, controller,
            text="Please Upload the JSON Template File : ",
            font=FONTS['LARGE_FONT'],
            x = 150, y = 0
        )

        upload_button = MyButton(
            head_wrapper, controller,
            command=self.upload_json_file_for_processing,
            text="Select File",
            font=FONTS['BUTTON_FONT'],
            width=20,
            x = 500,
            y = 0
        )

        self.file_name_label = MyLabel(
            head_wrapper, controller,
            text="",
            font=FONTS['FILE_NAME_PREVIEW'],
            x=100, y = 50
        )
        

        body_wrapper = MyLabelFrame(self, controller, text="Body", height="200", expand=Y)
        
        preview_text_scroll_y = MyScrollBar(body_wrapper, controller, orient="vertical", side=RIGHT)
        
        preview_text_scroll_x = MyScrollBar(body_wrapper, controller, orient="horizontal", side=BOTTOM, fill=X)

        self.json_preview_text = MyText(body_wrapper, controller, width=10, height="10", wrap="none", sticky=NSEW)
        
        preview_text_scroll_y.config(command=self.json_preview_text.yview)
        
        preview_text_scroll_x.config(command=self.json_preview_text.xview)

        self.json_preview_text.config( yscrollcommand=preview_text_scroll_y.set, xscrollcommand=preview_text_scroll_x.set)

        footer_wrapper = MyLabelFrame(self, controller, text="Footer", height ="50", expand=N)

        process_variables_button = Button(
            footer_wrapper,
            text="Process Variables",
            command=lambda:controller.show_frame(ProcessVariables)
        )
        process_variables_button.pack(pady=10, padx=10)

    def upload_json_file_for_processing(self):
        try:
            self.get_json_file_name()
            self.get_json_data()
            self.preview_json_data()
            self.update_file_name_preview()

        except FileNotFoundError:
            print("File not Selected or Not Found..")
        finally:
            pass

    def get_json_file_name(self):
        self.controller.TEMPLATE_JSON_FILE = filedialog.askopenfilename(
            initialdir = self.controller.current_dir    ,
            title = "Select a File",
            filetypes = ACCEPTABLE_FILE_TYPES
        )

    def get_json_data(self):
        with open(self.controller.TEMPLATE_JSON_FILE, mode="r") as json_file:
            self.controller.json_data = json.load(json_file)
            self.controller.JSON_STR_TO_PRINT = json.dumps(self.controller.json_data, indent=JSON_PREVIEW_INDENT)
            self.controller.JSON_STR = json.dumps(self.controller.json_data)
            self.controller.VARIABLES_PRESENT = ProcessData.get_all_variables(self.controller.JSON_STR)

    def preview_json_data(self):
        self.json_preview_text.config(state="normal")
        self.json_preview_text.delete("1.0",END)
        self.json_preview_text.insert(END, self.controller.JSON_STR_TO_PRINT)
        self.json_preview_text.config(state="disabled")
        
    def update_file_name_preview(self):
        self.file_name_label.configure(text=f"File : {self.controller.TEMPLATE_JSON_FILE}")
        

class ProcessVariables(Frame):

    def __init__(self, parent, controller:JsonTestCaseTracker):
        Frame.__init__(self, parent)

        

        test_label = Label(self, text="Process", font = FONTS["LARGE_FONT"])
        test_label.pack(padx=10, pady=10)

        

        button1 = Button(
            self,
            text="Goto Page 1",
            command=lambda:controller.show_frame(UploadPage)
        )
        button1.pack(pady=10, padx=10)


class MyLabelFrame(LabelFrame):
    def __init__(
        self,
        parent,
        controller : JsonTestCaseTracker,
        text:str=DEF_LABELFRAME_TEXT,
        height:str=DEF_LABELFRAME_HEIGHT,
        expand:str=DEF_LABELFRAME_EXPAND
    ):
        LabelFrame.__init__(self, parent, text=text, height=height)

        self.pack(fill=DEF_LABELFRAME_FILL, expand=expand)


class MyLabel(Label):

    def __init__(
        self,
        parent,
        controller :JsonTestCaseTracker,
        text:str=DEF_LABEL_TEXT,
        font = None,
        x:int = None,
        y:int = None
    ):
        Label.__init__(self, parent, text=text, font=tkfont.Font(**FONTS['LABEL_FONT']))

        if x is not None and y is not None:
            self.place(x=x, y=y)


class MyButton(Button):

    def __init__(
        self,
        parent,
        controller : JsonTestCaseTracker,
        text : str = DEF_BUTTON_TEXT,
        command = DEF_BUTTON_FUNC,
        width:int = DEF_BUTTON_WIDTH,
        font=FONTS['BUTTON_FONT'],
        x = None,
        y = None
    ):
        Button.__init__(
            self,
            parent,
            text=text,
            command=command,
            width= width,
            font=tkfont.Font(**font)
        )

        # if font is None:
        #     font = FONTS['BUTTON_FONT']
        # self['font'] = FONTS['BUTTON_FONT']
        # self.config(font = font)
        if x is not None and y is not None:
            self.place(x=x, y=y)


class MyText(Text):

    def __init__(
        self,
        parent,
        controller:JsonTestCaseTracker,
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


class MyScrollBar(Scrollbar):

    def __init__(
        self,
        parent,
        controller:JsonTestCaseTracker,
        command = None,
        orient:str="vertical",
        side:str=RIGHT, fill:str=Y
    ):
        Scrollbar.__init__(self, parent, orient=orient)
        self.pack(side=side, fill=fill)
        if command:
            self.config(command=command)


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

# 
# 
# 
# 
# 


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

app = JsonTestCaseTracker()
app.mainloop()
