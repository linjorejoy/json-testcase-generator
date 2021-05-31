from tkinter import Frame, filedialog
from tkinter import N, NW, SE, SW, NSEW, X, Y, RIGHT, BOTTOM, END
import json
import os

from widgetclasses.MyLabelFrame import MyLabelFrame
from widgetclasses.MyLabel import MyLabel
from widgetclasses.MyButton import MyButton
from widgetclasses.MyScrollBar import MyScrollBar
from widgetclasses.MyText import MyText

from helpermodules.constants import JSON_PREVIEW_INDENT, ACCEPTABLE_FILE_TYPES
from helpermodules.MyFonts import FONTS

import helpermodules.ProcessData as ProcessData 

import pages.TableProcessVariables as TableProcessVariables

import JSON_Test_Case_Generator

class TableUploadPage(Frame):

    def __init__(self, parent, controller):

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

        prev_frame_button = MyButton(
            footer_wrapper,
            controller,
            text="Go Back",
            command=self.go_back,
            x=5,
            y=-5,
            relx=0,
            rely=1.0,
            anchor=SW
        )

        process_variables_button = MyButton(
            footer_wrapper,
            controller,
            text="Process Variables",
            command=self.goto_next,
            x=-5,
            y=-5,
            relx=1.0,
            rely=1.0,
            anchor=SE
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
    
    def go_back(self):
        self.controller.go_back()

    def goto_next(self):
        self.controller.show_frame(TableProcessVariables.TableProcessVariables)
        # self.controller.frames[TableProcessVariables.TableProcessVariables].set_ui()
        
    def set_ui(self):
        print("UploadPage : set_ui")
