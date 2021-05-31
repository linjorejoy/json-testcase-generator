from tkinter import Frame, StringVar, Button
from tkinter import N, Y, SE, SW, NSEW, BOTH

import sys

from functools import partial

from widgetclasses.MyLabelFrame import MyLabelFrame
from widgetclasses.MyButton import MyButton
from widgetclasses.MyLabel import MyLabel
from widgetclasses.MyEntry import MyEntry
from widgetclasses.DoubleScrolledFrame import DoubleScrolledFrame
from widgetclasses.EntryWithType import EntryWithType

from helperobjects.EntryCellRow import EntryCellRow
from helperobjects.EntryCell import EntryCell
from helperobjects.OutputJsonFile import OutputJsonFile

from helpermodules.constants import INT_MAX_VALUE
from helpermodules.MyFonts import FONTS
import helpermodules.DataTypeHandler as DataTypeHandler
import helpermodules.PreferencesJsonHandler as PreferencesJsonHandler
import pages.TableSetNames as TableSetNames

import JSON_Test_Case_Generator



class TableProcessVariables(Frame):

    def __init__(self, parent, controller):

        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.entryrow_children_dict = {}
        self.added_widgets = []

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
        button_prev = MyButton(
            self.footer_label_frame,
            controller,
            text="Go Back",
            command=self.go_back,
            x=5,
            y=-5,
            relx=0,
            rely=1.0,
            anchor=SW
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

    def set_ui(self):
        self.clear_prev_widgets()
        self.clear_other_objects()
        self.set_row_initialization()
        self.set_headings()
        self.set_first_set_entry()
        self.set_add_more_empty_button()

    def clear_prev_widgets(self):
        for widget in self.added_widgets:
            widget.destroy()
        self.added_widgets = []

    def clear_other_objects(self):
        self.entryrow_children_dict.clear()

    def set_row_initialization(self):
        self.controller.entry_cell_collection.clear_all_rows()
        entry_row_0 = EntryCellRow()
        
        self.controller.entry_cell_collection.entry_cell_rows =[entry_row_0]

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
            self.added_widgets.append(header)
            self.controller.entry_cell_collection.entry_cell_rows[0].add_cell(EntryCell())
        commnet_entry_width = int(PreferencesJsonHandler.get_data_from_settings("additionalCommentEntryWidth"))
        comment_header = MyLabel(
            self.body_scrollable,
            self.controller,
            text="Additional Comment" + " "*commnet_entry_width,
            font=FONTS['LARGE_FONT'],
            grid=(0, len(self.controller.VARIABLES_PRESENT) + 2),
            padx=0,
            pady=0
        )
        self.added_widgets.append(comment_header)

    def set_first_set_entry(self):

        for row_index, row in enumerate(self.controller.entry_cell_collection.entry_cell_rows):
            
            copy_row_button = MyButton(
                self.body_scrollable,
                self.controller,
                text="Copy Row",
                command=partial(self.copy_row, row),
                grid=(row_index + 1, 0),
                padx=4,
                pady=2
            )
            self.added_widgets.append(copy_row_button)
            self.entryrow_children_dict[row] = []
            self.entryrow_children_dict[row].append(copy_row_button)

            for col_index, cell in enumerate(row.get_all()):
                cell.option_value = StringVar(value="str")
                entry_0 = EntryWithType(
                    self.body_scrollable,
                    self.controller,
                    frame_name="",
                    entry_cell=cell,
                    options=self.controller.accepted_data_types,
                    add_del_button=False,
                    grid=(row_index + 1, col_index + 2),
                    padx=1,
                    pady=1
                )
                self.added_widgets.append(entry_0)
                
                self.entryrow_children_dict[row].append(entry_0)

            row.comment_entry = EntryCell()
            # comment_entry_cell = EntryCell()
            row.comment_entry.option_value = StringVar(value="str")
            comment_entry = EntryWithType(
                self.body_scrollable,
                self.controller,
                frame_name="",
                entry_cell=row.comment_entry,
                options=self.controller.accepted_data_types,
                add_del_button=False,
                grid=(row_index + 1, len(row.get_all()) + 2),
                padx=1,
                pady=2,
                width=150
            )
            # self.body_scrollable.grid_columnconfigure(len(row.get_all()) + 2, weight=1)
            self.added_widgets.append(comment_entry)
            self.entryrow_children_dict[row].append(comment_entry)
                      
    def delete_row(self, entry_row:EntryCellRow):
        self.controller.entry_cell_collection.delete_row(entry_row)
        for widget in self.entryrow_children_dict[entry_row]:
            widget.destroy()
        
    def set_add_more_empty_button(self):
        if len(self.controller.VARIABLES_PRESENT) > 0:

            add_more_button = MyButton(
                self.body_scrollable,
                self.controller,
                command=self.add_one_row,
                text="Add more Empty",
                grid=(INT_MAX_VALUE, 2),
                columnspan=len(self.controller.VARIABLES_PRESENT) + 1,
                sticky=NSEW
            )
            self.added_widgets.append(add_more_button)
    


    def add_one_row(self):
        current_row_count = len(self.controller.entry_cell_collection.get_all_rows())
        entry_row = EntryCellRow()
        self.entryrow_children_dict[entry_row] = []

        

        copy_row_button = MyButton(
            self.body_scrollable,
            self.controller,
            text="Copy Row",
            command=partial(self.copy_row, entry_row),
            grid=(current_row_count + 1, 0),
            padx=4,
            pady=2
        )

        del_row_button = MyButton(
            self.body_scrollable,
            self.controller,
            text="Delete Row",
            command=partial(self.delete_row, entry_row),
            grid=(current_row_count + 1, 1),
            padx=4,
            pady=2
        )
        self.added_widgets.append(copy_row_button)
        self.added_widgets.append(del_row_button)
        self.entryrow_children_dict[entry_row].append(copy_row_button)
        self.entryrow_children_dict[entry_row].append(del_row_button)

        for index, value in enumerate(self.controller.VARIABLES_PRESENT):
            entry_cell = EntryCell()
            entry_cell.option_value = StringVar(value="str")
            entry_n = EntryWithType(
                self.body_scrollable,
                self.controller,
                frame_name="",
                entry_cell=entry_cell,
                options=self.controller.accepted_data_types,
                add_del_button=False,
                grid=(current_row_count + 1, index + 2),
                padx=1,
                pady=1
            )
            self.added_widgets.append(entry_n)
            self.entryrow_children_dict[entry_row].append(entry_n)
            
            entry_row.add_cell(entry_cell)
        entry_row.comment_entry = EntryCell()
        entry_row.comment_entry.option_value = StringVar(value="str")
        comment_entry = EntryWithType(
            self.body_scrollable,
            self.controller,
            frame_name="",
            entry_cell=entry_row.comment_entry,
            options=self.controller.accepted_data_types,
            add_del_button=False,
            grid=(current_row_count + 1, len(self.controller.VARIABLES_PRESENT) + 2),
            padx=1,
            pady=1,
            width=50
        )
        self.added_widgets.append(comment_entry)
        self.entryrow_children_dict[entry_row].append(comment_entry)

        self.controller.entry_cell_collection.add_row(entry_row)

    def copy_row(self, entry_row:EntryCellRow):
        current_row_count = len(self.controller.entry_cell_collection.get_all_rows())
        new_entry_row = EntryCellRow()
        self.entryrow_children_dict[new_entry_row] = []

        entries_entered = entry_row.get_all()

        copy_row_button = MyButton(
            self.body_scrollable,
            self.controller,
            text="Copy Row",
            command=partial(self.copy_row, new_entry_row),
            grid=(current_row_count + 1, 0),
            padx=4,
            pady=2
        )

        del_row_button = MyButton(
            self.body_scrollable,
            self.controller,
            text="Delete Row",
            command=partial(self.delete_row, new_entry_row),
            grid=(current_row_count + 1, 1),
            padx=4,
            pady=2
        )
        self.added_widgets.append(copy_row_button)
        self.added_widgets.append(del_row_button)
        self.entryrow_children_dict[new_entry_row].append(copy_row_button)
        self.entryrow_children_dict[new_entry_row].append(del_row_button)

        for index, value in enumerate(self.controller.VARIABLES_PRESENT):
            entry_cell = EntryCell()
            entry_cell.option_value = StringVar(value="str")
            entry_n = EntryWithType(
                self.body_scrollable,
                self.controller,
                frame_name="",
                entry_cell=entry_cell,
                entry_def_value=entries_entered[index].entry.get(),
                options=self.controller.accepted_data_types,
                add_del_button=False,
                grid=(current_row_count + 1, index + 2),
                padx=1,
                pady=1
            )
            self.added_widgets.append(entry_n)
            self.entryrow_children_dict[new_entry_row].append(entry_n)
            
            new_entry_row.add_cell(entry_cell)

        new_entry_row.comment_entry = EntryCell()
        new_entry_row.comment_entry.option_value = StringVar(value="str")
        comment_entry = EntryWithType(
            self.body_scrollable,
            self.controller,
            frame_name="",
            entry_cell=new_entry_row.comment_entry,
            entry_def_value=entry_row.comment_entry.entry.get(),
            options=self.controller.accepted_data_types,
            add_del_button=False,
            grid=(current_row_count + 1, len(self.controller.VARIABLES_PRESENT) + 2),
            padx=1,
            pady=1,
            width=50
        )
        self.added_widgets.append(comment_entry)
        self.entryrow_children_dict[new_entry_row].append(comment_entry)

        
        self.controller.entry_cell_collection.add_row(new_entry_row)


    def genetrate_output_files(self):
        self.controller.output_files.clear_output_json_file_arr()

        for row in self.controller.entry_cell_collection.get_all_rows():
            this_variable_dictionary = DataTypeHandler.genetrate_variable_dictionary(
                self.controller.VARIABLES_PRESENT,
                row.entry_cell_list
            )
            this_json_file = OutputJsonFile(
                file_name=None, 
                variable_dictionary=this_variable_dictionary, 
                comment=row.comment_entry.entry.get()
            )
            self.controller.output_files.add_output_json_file(this_json_file)
    
    def go_back(self):
        self.controller.go_back()

    def goto_next(self):
        self.genetrate_output_files()
        self.controller.show_frame(TableSetNames.TableSetNames)
        # self.controller.frames[TableSetNames.TableSetNames].set_ui()