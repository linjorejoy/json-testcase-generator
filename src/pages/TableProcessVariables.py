from tkinter import Frame
from tkinter import N, Y, SE, NSEW, BOTH

import sys

from widgetclasses.MyLabelFrame import MyLabelFrame
from widgetclasses.MyButton import MyButton
from widgetclasses.MyLabel import MyLabel
from widgetclasses.MyEntry import MyEntry
from widgetclasses.DoubleScrolledFrame import DoubleScrolledFrame

from helperobjects.EntryCellRow import EntryCellRow
from helperobjects.EntryCell import EntryCell
from helperobjects.OutputJsonFile import OutputJsonFile

from helpermodules.constants import INT_MAX_VALUE
from helpermodules.MyFonts import FONTS

import pages.TableSetNames as TableSetNames

import JSON_Test_Case_Generator



class TableProcessVariables(Frame):

    def __init__(self, parent, controller):

        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.header_label_frame = MyLabelFrame(
            self,
            controller,
            text="Options",
            height="50",
            expand=N
        )
        

        self.body_label_frame = MyLabelFrame(
            self,
            controller,
            text="Options",
            height="500",
            expand=Y
        )

        self.body_scrollable = DoubleScrolledFrame(
            self.body_label_frame
        )
        self.body_scrollable.pack(fill=BOTH,expand=1)

        self.footer_label_frame = MyLabelFrame(
            self,
            controller,
            text="Options",
            height="50",
            expand=N
        )

        button_next = MyButton(
            self.footer_label_frame,
            controller,
            text="Process Variables",
            command=self.goto_next,
            x=-5,
            y=-5,
            relx=1.0,
            rely=1.0,
            anchor=SE
        )

    def goto_next(self):
        self.genetrate_output_files()
        self.controller.show_frame(TableSetNames.TableSetNames)
        self.controller.frames[TableSetNames.TableSetNames].set_ui()

    def set_ui(self):
        self.set_row_initialization()
        self.set_headings()
        self.set_first_set_entry()
        self.set_add_more_empty_button()

    def set_row_initialization(self):
        del self.controller.entry_cell_collection.entry_cell_rows
        entry_row_0 = EntryCellRow()
        self.controller.entry_cell_collection.entry_cell_rows =[entry_row_0]
        # self.controller.entry_cell_collection.entry_cell_rows =[entry_row_0]


    def set_headings(self):
        for index, var in enumerate(self.controller.VARIABLES_PRESENT):

            header = MyLabel(
                self.body_scrollable,
                self.controller,
                text=var,
                font=FONTS['LARGE_FONT'],
                grid=(0, index + 2),
                padx=0,
                pady=0
            )
            self.controller.entry_cell_collection.entry_cell_rows[0].add_cell(EntryCell())

    def set_first_set_entry(self):
        for row_index, row in enumerate(self.controller.entry_cell_collection.entry_cell_rows):
            for col_index, cell in enumerate(row.get_all()):
                entry_0 = MyEntry(
                    self.body_scrollable,
                    self.controller,
                    grid=(row_index + 1, col_index + 2),
                    padx=0,
                    pady=0,
                    sticky=NSEW
                )
                cell.entry = entry_0

    def set_add_more_empty_button(self):
        if len(self.controller.VARIABLES_PRESENT) > 0:

            add_more_button = MyButton(
                self.body_scrollable,
                self.controller,
                command=self.add_one_row,
                text="Add more Empty",
                grid=(INT_MAX_VALUE, 2),
                columnspan=len(self.controller.VARIABLES_PRESENT),
                sticky=NSEW
            )

    def add_one_row(self):
        current_row_count = len(self.controller.entry_cell_collection.get_all_rows())
        entry_row = EntryCellRow()
        for index, value in enumerate(self.controller.VARIABLES_PRESENT):
            entry_cell = EntryCell()
            # entry_row.add_cell(EntryCell())
            entry_n = MyEntry(
                self.body_scrollable,
                self.controller,
                grid=(current_row_count + 1, index + 2),
                padx=0,
                pady=0,
                sticky=NSEW
            )
            entry_cell.entry = entry_n
            entry_row.add_cell(entry_cell)
        self.controller.entry_cell_collection.add_row(entry_row)

        # print(len(self.controller.entry_cell_collection.get_all_rows()))

    def genetrate_output_files(self):
        self.controller.output_files.clear_output_json_file_arr()

        for row in self.controller.entry_cell_collection.get_all_rows():
            this_variable_dictionary = {
                var:entry_obj.entry.get()
             for var, entry_obj in zip(
                 self.controller.VARIABLES_PRESENT,
                 row.entry_cell_list
             )}
            this_json_file = OutputJsonFile(file_name=None, variable_dictionary=this_variable_dictionary)
            self.controller.output_files.add_output_json_file(this_json_file)
        
        # [print(json_file_obj.__dict__) for json_file_obj in self.controller.output_files.get_output_json_file_array()]


        