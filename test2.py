from tkinter import Tk, Frame, filedialog, LabelFrame, Scrollbar, OptionMenu, Checkbutton, Canvas, Widget
from tkinter import Text, Button, Label, Entry
from tkinter import IntVar, StringVar
from tkinter import ttk
import tkinter.font as tkfont
from tkinter.ttk import Combobox, Treeview, Progressbar
from tkinter import RIGHT, LEFT, END, BOTH, NONE, TOP, SW, NE, SE, NW, W, NSEW, BOTTOM, HORIZONTAL, VERTICAL
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
from helpermodules.constants import PADX, PADY
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


        FRAMES = [UploadPage, ProcessVariables, SetNames, PreviewVariables, GeneratePage]

        for FRAME in FRAMES:
            frame = FRAME(global_container, self)
            self.frames[FRAME] = frame
            frame.grid(row=0, column=0, sticky=NSEW)


        self.show_frame(UploadPage)


    def show_frame(self, FrameName):

        frame = self.frames[FrameName]
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

        # entry_0 = EntryWithType(head_wrapper, controller)
        
        upload_label = MyLabel(
            head_wrapper, controller,
            text="Please Upload the JSON Template File : ",
            font=FONTS['LARGE_FONT'],
            x = 150, y = 0, anchor=NW
        )

        upload_button = MyButton(
            head_wrapper, controller,
            command=self.upload_json_file_for_processing,
            text="Select File",
            font=FONTS['BUTTON_FONT'],
            width=20,
            x = 500,
            y = 0,
            anchor=NW
        )

        self.file_name_label = MyLabel(
            head_wrapper, controller,
            text="",
            font=FONTS['FILE_NAME_PREVIEW'],
            x=100, y = 50, anchor=NW
        )
        

        body_wrapper = MyLabelFrame(self, controller, text="Body", height="200", expand=Y)
        
        preview_text_scroll_y = MyScrollBar(body_wrapper, controller, orient="vertical", side=RIGHT)
        
        preview_text_scroll_x = MyScrollBar(body_wrapper, controller, orient="horizontal", side=BOTTOM, fill=X)

        self.json_preview_text = MyText(body_wrapper, controller, width=10, height="10", wrap="none", sticky=NSEW)
        
        preview_text_scroll_y.config(command=self.json_preview_text.yview)
        
        preview_text_scroll_x.config(command=self.json_preview_text.xview)

        self.json_preview_text.config( yscrollcommand=preview_text_scroll_y.set, xscrollcommand=preview_text_scroll_x.set)

        footer_wrapper = MyLabelFrame(self, controller, text="Footer", height ="50", expand=N)

        process_variables_button = MyButton(
            footer_wrapper,
            controller,
            text="Process Variables",
            command=self.goto_next,
            x=-5,
            y=-5,
            relx=1.0,
            rely=1.0,anchor=SE
        )
        
        

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
        
    def goto_next(self):
        self.controller.show_frame(ProcessVariables)
        self.controller.frames[ProcessVariables].set_ui()
        
    def set_ui(self):
        print("UploadPage : set_ui")


class ProcessVariables(Frame):

    def __init__(self, parent, controller:JsonTestCaseTracker):
        Frame.__init__(self, parent)
        self.controller = controller
        self.table_start_row = 1


        self.head_label_frame = MyLabelFrame(
            self, 
            controller,
            text="Stats",
            height="50",
            expand=N
        )

        test_label = Label(self.head_label_frame, text="Process", font = FONTS["LARGE_FONT"])
        test_label.pack(padx=10, pady=10)


        self.body_label_frame = MyLabelFrame(
            self, 
            controller,
            text="Variables",
            height="50",
            expand=Y
        )
        

        self.body_subframe = DoubleScrolledFrame(self.body_label_frame)

        self.footer_label_frame = MyLabelFrame(
            self, 
            controller,
            text="Goto",
            height="50",
            expand=N
        )


        button_prev = MyButton(
            self.footer_label_frame,
            controller,
            text="Go Back",
            command=lambda:controller.show_frame(UploadPage),
            rely=1,
            relx=0,
            x=5,
            y=-5,
            anchor=SW
        )


        button_next = MyButton(
            self.footer_label_frame,
            controller,
            text="Name Selection",
            command=self.goto_next,
            rely=1.0,
            relx=1.0,
            x=-5,
            y=-5,
            anchor=SE
        )
    

    def set_ui(self):
        self.create_entry_columns()


    def create_entry_columns(self):
        for index, variable in enumerate(self.controller.VARIABLES_PRESENT):
            this_var_entry_col = EntryCellColumn(variable_name=variable)
            this_var_entry_col_cell = EntryCell()
            this_var_entry_col.add_cell(entry_cell = this_var_entry_col_cell)
            self.controller.entry_cell_collection.add_column(this_var_entry_col)
            self.add_widget_for_col(index, variable, this_var_entry_col)
            self.body_subframe.pack(side="top", fill="both", expand=True)


    def add_widget_for_col(self, index, variable, this_var_entry_col):

        this_processdata_variable_add_cell_button = MyButton(
            self.body_subframe,
            self.controller,
            text="Add Cell",
            command=partial(self.add_cell, this_var_entry_col, index),
            width="15",
            grid=(0, (index + 1)),
            pady=2,
            padx=3
        )
        this_processdata_variable_header = MyLabel(
            self.body_subframe,
            self.controller,
            text=variable,
            font=FONTS['LABEL_FONT'],
            grid=(self.table_start_row, (index+1)),
            pady=2,
            padx=3
        )

        for yindex, cell in enumerate(this_var_entry_col.entry_cell_column):
            this_entry = MyEntry(
                self.body_subframe,
                self.controller,
                grid=((yindex+self.table_start_row+1),(index+1)),
                pady=1,
                padx=8
            )
            cell.entry = this_entry
        

    def add_cell(self, entry_col:EntryCellColumn, index:int):

        this_cell = EntryCell()
        yindex = entry_col.add_cell(this_cell)
        this_entry = MyEntry(
            self.body_subframe,
            self.controller,
            grid = ((yindex + 2), (index + 1)),
            pady=1,
            padx=8
        )
        this_cell.entry = this_entry
    
    def generate_output_file_obj(self):
        for column in self.controller.entry_cell_collection.entry_cells_collection:
            for cell in column.entry_cell_column:
                cell.value = cell.entry.get()
        
        all_combinations = GetAllCombinations.get_all_dictionaries(self.controller.entry_cell_collection)

        [(
            self.controller.output_files.add_output_json_file(OutputJsonFile(variable_dictionary=combination))
        ) for combination in all_combinations]

        [(
            print(combination)
        )for combination in all_combinations]



    def goto_next(self):
        self.generate_output_file_obj()
        self.controller.show_frame(SetNames)
        self.controller.frames[SetNames].set_ui()
        

class SetNames(Frame):

    def __init__(self, parent, controller:JsonTestCaseTracker):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        print(f"VARS PRESENT : {self.controller.VARIABLES_PRESENT} ")
        self.variables_for_dropdown = ["None", "Counter"]

        self.header_label_frame = MyLabelFrame(
            self,
            controller,
            text="Info",
            height="50",
            expand=N
        )

        test_label = Label(self.header_label_frame, text="Set Names", font = FONTS["LARGE_FONT"])
        test_label.pack(padx=10, pady=10)

        self.body_label_frame = MyLabelFrame(
            self,
            controller,
            text="Body",
            height="500",
            expand=Y
        )

        self.body_scrollable = DoubleScrolledFrame(self.body_label_frame)

        self.footer_label_frame = MyLabelFrame(
            self,
            controller,
            text="Footer",
            height="50",
            expand=N
        )

        button_prev = MyButton(
            self.footer_label_frame,
            controller,
            text="Go Back",
            command=lambda:controller.show_frame(ProcessVariables),
            rely=1,
            relx=0,
            x=5,
            y=-5,
            anchor=SW
        )


        button_next = MyButton(
            self.footer_label_frame,
            controller,
            text="Preview Results",
            command=self.goto_next,
            rely=1.0,
            relx=1.0,
            x=-5,
            y=-5,
            anchor=SE
        )

    def set_ui(self):
        
        self.variables_for_dropdown = ["None", "Counter", *self.controller.VARIABLES_PRESENT]
        entry_0 = MyEntry(
            self.body_scrollable,
            self.controller,
            grid=(0, 0)
        )
        self.controller.reference_arr_for_name_gen.append(entry_0)
        for index in range(len(self.variables_for_dropdown)):

            if not self.variables_for_dropdown:
                self.variables_for_dropdown = [""]
            
            plus_label_0 = MyLabel(
                self.body_scrollable,
                self.controller,
                text="+",
                font=FONTS['FONT_PLUS_SIGN'],
                grid=(index, 1)
            )

            this_dropdown_var = StringVar()
            this_dropdown_var.set(None)

            this_dropdown = MyOptionMenu(
                self.body_scrollable,
                self.controller,
                this_dropdown_var,
                options=self.variables_for_dropdown,
                grid=(index, 2),
                padx=1,
                pady=3
            )
            self.controller.reference_arr_for_name_gen.append(this_dropdown_var)
            
            plus_label_1 = MyLabel(
                self.body_scrollable,
                self.controller,
                text="+",
                font=FONTS['FONT_PLUS_SIGN'],
                grid=(index, 1)
            )

            entry_n = MyEntry(
                self.body_scrollable,
                self.controller,
                grid=(index, 4),
                padx=1,
                pady=3
            )
            self.controller.reference_arr_for_name_gen.append(entry_n)
        self.body_scrollable.pack(side="top", fill="both", expand=True)


    def goto_next(self):
        self.controller.show_frame(PreviewVariables)
        self.controller.frames[PreviewVariables].set_ui()


class PreviewVariables(Frame):

    def __init__(self, parent, controller:JsonTestCaseTracker):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.preview_tree_variables:list = None

        
        self.header_label_frame = MyLabelFrame(
            self,
            self.controller,
            text="Stats",
            height="80",
            expand=N
        )

        
        self.body_label_frame = MyLabelFrame(
            self,
            self.controller,
            text="All Variables",
            height="500",
            expand=Y
        )

        self.srollable_treeview_frame = DoubleScrolledFrame(self.body_label_frame)

        self.srollable_treeview_frame.pack(fill=BOTH, expand=True)

        # self.preview_tree = Treeview(self.srollable_treeview_frame)
        
        self.footer_label_frame = MyLabelFrame(
            self,
            self.controller,
            text="Options",
            height="80",
            expand=N
        )
        

        button_prev = MyButton(
            self.footer_label_frame,
            controller,
            text="Go Back",
            command=lambda:controller.show_frame(SetNames),
            rely=1,
            relx=0,
            x=5,
            y=-5,
            anchor=SW
        )


        button_next = MyButton(
            self.footer_label_frame,
            controller,
            text="Preview Results",
            command=self.goto_next,
            rely=1.0,
            relx=1.0,
            x=-5,
            y=-5,
            anchor=SE
        )

    
    def set_ui(self):
        self.generate_file_name_to_output_files()
        # self.destroy_preexisting_widgets()
        self.set_treeview()
        self.set_columns_treeview()
        self.set_headers_treeview()
        self.add_values_treeview()


    def generate_file_name_to_output_files(self):
        [(
            print(json_file_obj.__dict__)
        ) for json_file_obj in self.controller.output_files.get_output_json_file_array()]
        FileNameGenerator.generate_file_name(
            output_files=self.controller.output_files,
            ref_arr=self.controller.reference_arr_for_name_gen
        )
        [(
            print(json_file_obj.__dict__)
        ) for json_file_obj in self.controller.output_files.get_output_json_file_array()]
    

    def destroy_preexisting_widgets(self):

        for widget in self.srollable_treeview_frame.winfo_children():
            widget.destroy()
        

    def set_treeview(self):
        self.preview_tree = Treeview(self.srollable_treeview_frame)
        self.preview_tree_variables = ["File Name", *self.controller.VARIABLES_PRESENT]
        

        print(f"\n\n{self.preview_tree_variables}\n\n")

    def set_columns_treeview(self):
        self.preview_tree['columns'] = tuple(self.preview_tree_variables)
        self.preview_tree.column('#0', width=60, minwidth=45)

        for var in self.preview_tree_variables:
            self.preview_tree.column(var, width=150, anchor=W, minwidth=45)
        
    def set_headers_treeview(self):
        self.preview_tree.heading('#0', text="Count", anchor=W)
        for var in self.preview_tree_variables:
            self.preview_tree.heading(
                var,
                text=var.replace("$", "").title(),
                anchor=W
            )
    
    def add_values_treeview(self):
        for index, json_file_obj in enumerate(self.controller.output_files.get_output_json_file_array()):
            values_to_add_list = [json_file_obj.file_name, *json_file_obj.variable_dictionary.values()]
            values_to_add_tuple = tuple(values_to_add_list)
            self.preview_tree.insert(
                parent='',
                index='end',
                iid=index,
                text=index+1,
                values=values_to_add_tuple
            )
        self.preview_tree.pack(fill=BOTH, expand=True)


    def goto_next(self):
        self.controller.show_frame(GeneratePage)
        self.controller.frames[GeneratePage].set_ui()



class GeneratePage(Frame):

    def __init__(self, parent, controller:JsonTestCaseTracker):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.header_label_frame = MyLabelFrame(
            self,
            self.controller,
            text="Options",
            height="50",
            expand=N
        )

        select_output_loc_button = MyButton(
            self.header_label_frame,
            self.controller,
            text="Select Output Location",
            command=self.select_output_loc,
            width=50,
            grid=(0, 0),
            pady=5,
            padx=50
        )

        self.generate_output_button = MyButton(
            self.header_label_frame,
            self.controller,
            text="Generate",
            command=self.generate_outputs,
            width=50,
            grid=(0, 1),
            pady=5,
            padx=50,
            state="disabled"
        )

        self.body_label_frame = MyLabelFrame(
            self,
            self.controller,
            text="Options",
            height="500",
            expand=Y
        )

        self.generated_report = MyText(
            self.body_label_frame,
            controller,
            width=500,
            height=500,
            wrap=WORD,
            text="Click on Generate",
            sticky=NSEW
        )

        self.footer_label_frame = MyLabelFrame(
            self,
            self.controller,
            text="Options",
            height="50",
            expand=N
        )



        button_prev = MyButton(
            self.footer_label_frame,
            controller,
            text="Go Back",
            command=lambda:controller.show_frame(PreviewVariables),
            rely=1,
            relx=0,
            x=5,
            y=-5,
            anchor=SW
        )


        button_next = MyButton(
            self.footer_label_frame,
            controller,
            text="Restart",
            command=self.goto_next,
            rely=1.0,
            relx=1.0,
            x=-5,
            y=-5,
            anchor=SE
        )
    
    def select_output_loc(self):
        
        self.controller.output_location = filedialog.askdirectory(
            initialdir = self.controller.current_dir,
            title = "Select Output Directory"
        )
        self.generate_output_button.config(state="normal")

    def generate_outputs(self):
        progress_bar_length = 300
        
        progress_bar = Progressbar(self.header_label_frame, orient="horizontal", length=progress_bar_length)
        progress_bar.grid(row=1, column=0, columnspan=2)

        num_files = self.controller.output_files.count
        progress_jump = int(progress_bar_length // num_files)

        for json_file_obj in self.controller.output_files.get_output_json_file_array():
            self.generated_report.config(state="normal")
            self.generated_report.insert(END, f"\n{json_file_obj.file_name:>50}............Creating")
            self.generated_report.config(state="disabled")
            GenerateFile.generate_one_file(
                json_file_obj,
                self.controller.json_data,
                self.controller.output_location
            )
            progress_bar['value'] += progress_jump
            self.generated_report.config(state="normal")
            self.generated_report.insert(END, f"\n{json_file_obj.file_name:>50}............Done")
            self.generated_report.config(state="disabled")
        

    def set_ui(self):
        pass

    def goto_next(self):
        pass
    


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
        x:int = 0,
        y:int = 0,
        relx:int = 0,
        rely:int = 0,
        anchor=NE,
        grid=None,
        pady=PADY,
        padx=PADX
    ):
        Label.__init__(self, parent, text=text, font=tkfont.Font(**FONTS['LABEL_FONT']))

        if not grid:
            self.place(x=x, y=y, relx=relx, rely=rely, anchor=anchor)
        else:
            row, col = grid
            self.grid(row=row, column=col, pady=pady, padx=padx)


class MyButton(Button):

    def __init__(
        self,
        parent,
        controller : JsonTestCaseTracker,
        text : str = DEF_BUTTON_TEXT,
        command = DEF_BUTTON_FUNC,
        width:int = DEF_BUTTON_WIDTH,
        font=FONTS['BUTTON_FONT'],
        x = 0,
        y = 0,
        relx=0,
        rely=0,
        anchor=NE,
        grid = None,
        pady=PADY,
        padx=PADX,
        state="normal"
    ):
        Button.__init__(
            self,
            parent,
            text=text,
            command=command,
            width= width,
            font=tkfont.Font(**font),
            state=state
        )
        if not grid:
            self.place(rely=rely, relx=relx, x=x, y=y, anchor=anchor)
        else:
            row, col = grid
            self.grid(row=row, column=col, pady=pady, padx=padx)


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


class MyCanvas(Canvas):

    def __init__(
        self,
        parent,
        controller:JsonTestCaseTracker,
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


class MyOptionMenu(OptionMenu):

    def __init__(
        self,
        parent,
        controller:JsonTestCaseTracker,
        variable:StringVar,
        options:list=["No","Options","Given"],
        x = 0,
        y = 0,
        relx=0,
        rely=0,
        grid = None,
        pady=PADY,
        padx=PADX
    ):
        OptionMenu.__init__(self, parent, variable, *options)
        if grid:
            row, col = grid
            self.grid(row=row, column=col, padx=padx, pady=pady)
        else:
            self.place(rely=rely, relx=relx, x=x, y=y, anchor=anchor)



class EntryWithType(LabelFrame):
    def __init__(
        self,
        parent,
        controller:JsonTestCaseTracker,
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


        

class MyEntry(Entry):

    def __init__(
        self,
        parent,
        controller:JsonTestCaseTracker,
        x = 0,
        y = 0,
        relx=0,
        rely=0,
        anchor=NW,
        grid = None,
        pady=PADY,
        padx=PADX

    ):
        Entry.__init__(self, parent)
        if not grid:
            self.place(rely=rely, relx=relx, x=x, y=y, anchor=anchor)
        else:
            row, col = grid
            self.grid(row=row, column=col, pady=pady, padx=padx)


class DoubleScrolledFrame:

    def __init__(self, master, **kwargs):
        width = kwargs.pop('width', None)
        height = kwargs.pop('height', None)
        self.outer = Frame(master, **kwargs)

        self.vsb = Scrollbar(self.outer, orient=VERTICAL)
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.hsb = Scrollbar(self.outer, orient=HORIZONTAL)
        self.hsb.grid(row=1, column=0, sticky='ew')
        self.canvas = Canvas(self.outer, highlightthickness=0, width=width, height=height)
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.outer.rowconfigure(0, weight=1)
        self.outer.columnconfigure(0, weight=1)
        self.canvas['yscrollcommand'] = self.vsb.set
        self.canvas['xscrollcommand'] = self.hsb.set

        self.canvas.bind("<Enter>", self._bind_mouse)
        self.canvas.bind("<Leave>", self._unbind_mouse)

        self.vsb['command'] = self.canvas.yview
        self.hsb['command'] = self.canvas.xview

        self.inner = Frame(self.canvas)
        
        self.canvas.create_window(4, 4, window=self.inner, anchor='nw')
        self.inner.bind("<Configure>", self._on_frame_configure)

        self.outer_attr = set(dir(Widget))

    def __getattr__(self, item):
        if item in self.outer_attr:
            
            return getattr(self.outer, item)
        else:
            
            return getattr(self.inner, item)

    def _on_frame_configure(self, event=None):
        x1, y1, x2, y2 = self.canvas.bbox("all")
        height = self.canvas.winfo_height()
        width = self.canvas.winfo_width()
        self.canvas.config(scrollregion = (0,0, max(x2, width), max(y2, height)))

    def _bind_mouse(self, event=None):
        self.canvas.bind_all("<4>", self._on_mousewheel)
        self.canvas.bind_all("<5>", self._on_mousewheel)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mouse(self, event=None):
        self.canvas.unbind_all("<4>")
        self.canvas.unbind_all("<5>")
        self.canvas.unbind_all("<MouseWheel>")
        
    def _on_mousewheel(self, event):
        
        func = self.canvas.xview_scroll if event.state & 1 else self.canvas.yview_scroll 
        if event.num == 4 or event.delta > 0:
            func(-1, "units" )
        elif event.num == 5 or event.delta < 0:
            func(1, "units" )
    
    def __str__(self):
        return str(self.outer)




# 
# 
# 
# 
# 


class StartPage(Frame):

    def __init__(self, parent, controller:JsonTestCaseTracker):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.subframe = MyLabelFrame(
            self,
            controller,
            text="Main",
            height="500",
            expand=Y
        )

        self.subframe_scrollable = DoubleScrolledFrame(self.subframe)
        for j in range(10):
            for i in range(20):
                EntryWithType(
                    self.subframe_scrollable,
                    controller,
                    frame_name=f"{i} {j} ",
                    options=["int", "str", "bool", "float"],
                    grid=(i, j)
                )
            
        self.subframe_scrollable.pack(side="top", fill="both", expand=True)

        test_label = Label(self, text="Page 0 : Hello World", font = FONTS["LARGE_FONT"])
        test_label.pack(padx=10, pady=10)

        button1 = Button(
            self,
            text="Goto Page 1",
            command=lambda:controller.show_frame(UploadPage)
        )
        button1.pack(pady=10, padx=10)
    
    def set_ui(self):
        pass

app = JsonTestCaseTracker()
app.mainloop()