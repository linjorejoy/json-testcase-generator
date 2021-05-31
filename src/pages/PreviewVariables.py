from tkinter import Frame
from tkinter.ttk import Treeview
from tkinter import N, Y, BOTH, SW, SE, W


from widgetclasses.MyLabelFrame import MyLabelFrame
from widgetclasses.MyButton import MyButton
from widgetclasses.DoubleScrolledFrame import DoubleScrolledFrame

import pages.SetNames as SetNames
import pages.GeneratePage as GeneratePage

import helpermodules.FileNameGenerator as FileNameGenerator

import JSON_Test_Case_Generator

class PreviewVariables(Frame):

    def __init__(self, parent, controller:JSON_Test_Case_Generator.JsonTestCaseTracker):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.preview_tree_variables:list = None
        self.widgets_added = []

        
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
            text="Generate Results",
            command=self.goto_next,
            rely=1.0,
            relx=1.0,
            x=-5,
            y=-5,
            anchor=SE
        )

    
    def set_ui(self):
        self.generate_file_name_to_output_files()
        self.destroy_preexisting_widgets()
        self.set_treeview()
        self.set_columns_treeview()
        self.set_headers_treeview()
        self.add_values_treeview()

    def destroy_preexisting_widgets(self):
        for widget in self.widgets_added:
            widget.destroy()


    def generate_file_name_to_output_files(self):
        
        FileNameGenerator.generate_file_name(
            output_files=self.controller.output_files,
            ref_arr=self.controller.reference_arr_for_name_gen
        )
    
        

    def set_treeview(self):
        self.preview_tree = Treeview(self.srollable_treeview_frame)
        self.widgets_added.append(self.preview_tree)
        self.preview_tree_variables = ["File Name", *self.controller.VARIABLES_PRESENT]
        

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
        self.controller.show_frame(GeneratePage.GeneratePage)
        # self.controller.frames[GeneratePage.GeneratePage].set_ui()

    def go_back(self):
        self.controller.go_back()
        