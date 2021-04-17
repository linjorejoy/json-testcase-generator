from tkinter import Frame, Button
from tkinter import Y, NSEW

import tkinter.font as tkfont

from widgetclasses.MyLabelFrame import MyLabelFrame

import pages.UploadPage as UploadPage

from helpermodules.MyFonts import FONTS

import JSON_Test_Case_Generator

class StartPage(Frame):

    def __init__(self, parent, controller:JSON_Test_Case_Generator.JsonTestCaseTracker):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.body_label_frame = MyLabelFrame(
            self,
            controller,
            text="DD",
            height="10",
            expand=Y
        )
        
        make_combination_tree_button = Button(
            self.body_label_frame,
            text="Make All Combinations",
            command=lambda:controller.show_frame(UploadPage.UploadPage),
            font=tkfont.Font(**FONTS['VERY_LARGE_FONT']),
            width=20,
            height=5
        )
        make_combination_tree_button.grid(row=0, column=0, padx=0, pady=0, ipadx=2, ipady=2, sticky=NSEW)
        
        make_combination_from_sheet = Button(
            self.body_label_frame,
            text="Make Combinations from Table",
            command=lambda:controller.show_frame(UploadPage.UploadPage),
            font=tkfont.Font(**FONTS['VERY_LARGE_FONT']),
            width=20,
            height=5
        )
        make_combination_from_sheet.grid(row=1, column=2, padx=0, pady=0, sticky=NSEW)

        self.body_label_frame.grid_columnconfigure(0, weight=1)
        self.body_label_frame.grid_columnconfigure(2, weight=1)
        
    
    def set_ui(self):
        pass
