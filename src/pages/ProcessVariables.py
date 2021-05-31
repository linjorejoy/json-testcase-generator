from tkinter import Frame, Label, StringVar, LabelFrame, Entry
from tkinter import N, Y, SW, SE, BOTH

from functools import partial


from widgetclasses.MyLabelFrame import MyLabelFrame
from widgetclasses.MyButton import MyButton
from widgetclasses.MyLabel import MyLabel
from widgetclasses.MyEntry import MyEntry
from widgetclasses.DoubleScrolledFrame import DoubleScrolledFrame
from widgetclasses.EntryWithType import EntryWithType

from helperobjects.EntryCellColumn import EntryCellColumn
from helperobjects.EntryCell import EntryCell
from helperobjects.OutputFiles import OutputFiles
from helperobjects.OutputJsonFile import OutputJsonFile

from helpermodules.MyFonts import FONTS
import helpermodules.GetAllCombinations as GetAllCombinations

import pages.UploadPage as UploadPage
import pages.SetNames as SetNames

import JSON_Test_Case_Generator

class ProcessVariables(Frame):

    def __init__(self, parent, controller:JSON_Test_Case_Generator.JsonTestCaseTracker):
        Frame.__init__(self, parent)
        self.controller = controller
        self.table_start_row = 1
        self.cell_entry_dict = {}


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
            height="500",
            expand=Y
        )
        

        self.body_subframe = DoubleScrolledFrame(self.body_label_frame)

        self.label_frame_columns = []

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
            command=self.go_back,
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
        self.controller.entry_cell_collection.clear_all_columns()
        self.cell_entry_dict = {}
        self.clear_previous_widgets()
        self.create_entry_columns()

    def clear_previous_widgets(self):
        for column in self.label_frame_columns:
            column.destroy()
        self.label_frame_columns = []

    def create_entry_columns(self):
        
        for index, variable in enumerate(self.controller.VARIABLES_PRESENT):
            this_var_entry_col = EntryCellColumn(variable_name=variable)
            this_var_entry_col_cell = EntryCell()
            this_var_entry_col_cell.option_value =StringVar(value="str")
            this_var_entry_col.add_cell(entry_cell = this_var_entry_col_cell)
            self.controller.entry_cell_collection.add_column(this_var_entry_col)
            self.body_subframe.pack(side="top", fill=BOTH, expand=True)
            self.add_widget_for_col(index, variable, this_var_entry_col)

    def add_widget_for_col(self, index, variable, this_var_entry_col):
        this_col_label_frame = LabelFrame(
            self.body_subframe,
            text=f"Variable {index + 1}",
            height="1500"
        )
        this_col_label_frame.grid(row=0, column=index, sticky="nw")
        # self.body_subframe.grid_rowconfigure(index, weight=1)

        self.label_frame_columns.append(this_col_label_frame)

        this_processdata_variable_add_cell_button = MyButton(
            self.label_frame_columns[index],
            self.controller,
            text="Add Cell",
            command=partial(self.add_cell, this_var_entry_col, index),
            width="15",
            grid=(0, 0),
            pady=2,
            padx=3
        )
        this_processdata_variable_header = MyLabel(
            self.label_frame_columns[index],
            self.controller,
            text=variable,
            font=FONTS['LABEL_FONT'],
            grid=(self.table_start_row, 0),
            pady=2,
            padx=3
        )

        for yindex, cell in enumerate(this_var_entry_col.entry_cell_column):
            
            this_entry = EntryWithType(
                self.label_frame_columns[index],
                self.controller,
                frame_name="",
                entry_cell=cell,
                add_del_button=False,
                options=self.controller.accepted_data_types,
                delete_command=partial(self.remove_cell_from_column,this_var_entry_col, cell),
                show_add_cell_button=True,
                add_cell_command=partial(self.copy_cell, this_var_entry_col, index, cell),
                grid=((yindex+self.table_start_row+1),0),
                pady=1,
                padx=8
            )
            self.cell_entry_dict[cell] = this_entry
            
    def remove_cell_from_column(self, entry_col:EntryCellColumn, cell:EntryCell):
        for index, entry_cell in enumerate(entry_col.entry_cell_column):
            if cell == entry_cell:
                del entry_col.entry_cell_column[index]
                self.cell_entry_dict[cell].destroy()
        
        

    def add_cell(self, entry_col:EntryCellColumn, index:int):

        this_cell = EntryCell()
        this_cell.option_value  = StringVar(value="str")
        yindex = entry_col.add_cell(this_cell)
        this_entry = EntryWithType(
            self.label_frame_columns[index],
            self.controller,
            frame_name="",
            entry_cell=this_cell,
            options=self.controller.accepted_data_types,
            delete_command=partial(self.remove_cell_from_column,entry_col, this_cell),
            show_add_cell_button=True,
            add_cell_command=partial(self.copy_cell, entry_col, index, this_cell),
            grid=((yindex+self.table_start_row+1),0),
            pady=1,
            padx=8
        )
        self.cell_entry_dict[this_cell] = this_entry

    def copy_cell(self, entry_col:EntryCellColumn, col_index:int, entry_cell:EntryCell):

        this_entry_with_type:EntryWithType = self.cell_entry_dict[entry_cell]
        value = this_entry_with_type.this_entry.get()

        new_entry_cell = EntryCell()
        new_entry_cell.option_value  = StringVar(value="str")
        yindex = entry_col.add_cell(new_entry_cell)

        this_entry = EntryWithType(
            self.label_frame_columns[col_index],
            self.controller,
            frame_name="",
            entry_cell=new_entry_cell,
            entry_def_value=value,
            options=self.controller.accepted_data_types,
            delete_command=partial(self.remove_cell_from_column,entry_col, new_entry_cell),
            show_add_cell_button=True,
            add_cell_command=partial(self.copy_cell, entry_col, col_index, new_entry_cell),
            grid=((yindex+self.table_start_row+1),0),
            pady=1,
            padx=8
        )
        self.cell_entry_dict[new_entry_cell] = this_entry
    
    def generate_output_file_obj(self):
        self.controller.output_files.clear_output_json_file_arr()
        for column in self.controller.entry_cell_collection.entry_cells_collection:
            for cell in column.entry_cell_column:
                cell.value = cell.entry.get()
        
        all_combinations = GetAllCombinations.get_all_dictionaries(self.controller.entry_cell_collection)

        [(
            self.controller.output_files.add_output_json_file(OutputJsonFile(variable_dictionary=combination))
        ) for combination in all_combinations]




    def goto_next(self):
        self.generate_output_file_obj()
        self.controller.show_frame(SetNames.SetNames)
        # self.controller.frames[SetNames.SetNames].set_ui()

    def go_back(self):
        self.controller.go_back()