from tkinter import Frame, filedialog
from tkinter.ttk import Progressbar
from tkinter import N, Y, WORD, NSEW, SW, SE, END
import json
import datetime
import os

from widgetclasses.MyLabelFrame import MyLabelFrame
from widgetclasses.MyButton import MyButton
from widgetclasses.MyText import MyText

import pages.PreviewVariables as PreviewVariables

import helpermodules.GenerateFile as GenerateFile
import helpermodules.FileNameGenerator as FileNameGenerator
import helpermodules.PreferencesJsonHandler as PreferencesJsonHandler

import JSON_Test_Case_Generator

class GeneratePage(Frame):

    def __init__(self, parent, controller:JSON_Test_Case_Generator.JsonTestCaseTracker):
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
            self.generated_report.insert(END, f"\n{json_file_obj.temp_file_name:<50}............Creating")
            self.generated_report.config(state="disabled")
            GenerateFile.generate_one_file(
                json_file_obj,
                self.controller.json_data,
                self.controller.output_location
            )
            progress_bar['value'] += progress_jump
            self.generated_report.config(state="normal")
            self.generated_report.insert(END, f"\n{json_file_obj.temp_file_name:<50}............Done")
            self.generated_report.config(state="disabled")

        report_prefix = PreferencesJsonHandler.get_data_from_settings("reportJsonPrefix")
        report_prefix = FileNameGenerator.autocorrect_filename(report_prefix)
        time_str = str(datetime.datetime.now()).replace(":","-")
        report_file_name = f"{report_prefix} {time_str}.json"
        report_loc = os.path.join(self.controller.output_location, report_file_name)

        indent_from_settings = int(PreferencesJsonHandler.get_data_from_settings("spacesForTabs"))
        
        with open(report_loc, mode="w") as json_file:
            json.dump(
                self.controller.output_files.dictionary(),
                json_file,
                indent=indent_from_settings
            )

    def to_dict(self,obj):
        return json.dumps(obj, default=lambda o: o.__dict__, indent=2)

    def set_ui(self):
        pass

    def goto_next(self):
        self.controller.restart()

    def go_back(self):
        self.controller.go_back()
