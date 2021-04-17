from tkinter import Frame, Label
from tkinter import N, Y, SW, SE

from functools import partial


from widgetclasses.MyLabelFrame import MyLabelFrame
from widgetclasses.MyButton import MyButton
from widgetclasses.MyLabel import MyLabel
from widgetclasses.MyEntry import MyEntry
from widgetclasses.DoubleScrolledFrame import DoubleScrolledFrame

from helperobjects.EntryCellColumn import EntryCellColumn
from helperobjects.EntryCell import EntryCell
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
            command=lambda:controller.show_frame(UploadPage.UploadPage),
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

        # [(
        #     print(combination)
        # )for combination in all_combinations]



    def goto_next(self):
        self.generate_output_file_obj()
        self.controller.show_frame(SetNames.SetNames)
        self.controller.frames[SetNames.SetNames].set_ui()
