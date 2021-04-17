from tkinter import Frame
from tkinter import N, Y, SE, NSEW

import sys

from widgetclasses.MyLabelFrame import MyLabelFrame
from widgetclasses.MyButton import MyButton
from widgetclasses.MyLabel import MyLabel
from widgetclasses.MyEntry import MyEntry

from helperobjects.EntryCellRow import EntryCellRow
from helperobjects.EntryCell import EntryCell

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
        self.controller.show_frame(TableSetNames.TableSetNames)
        pass

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
                self.body_label_frame,
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
                    self.body_label_frame,
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
                self.body_label_frame,
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
                self.body_label_frame,
                self.controller,
                grid=(current_row_count + 1, index + 2),
                sticky=NSEW
            )
            entry_cell.entry = entry_n
            entry_row.add_cell(entry_cell)
        self.controller.entry_cell_collection.add_row(entry_row)

        print(len(self.controller.entry_cell_collection.get_all_rows()))