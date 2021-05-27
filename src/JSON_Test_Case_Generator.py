from tkinter import Tk, Frame, Menu
from tkinter import BOTH, TOP, NSEW

import os
import json
from pathlib import Path

from helperobjects.EntryCellCollection import EntryCellCollection
from helperobjects.EntryCellColumn import EntryCellColumn
from helperobjects.OutputJsonFile import OutputJsonFile
from helperobjects.OutputFiles import OutputFiles
from helperobjects.EntryCell import EntryCell

import pages.StartPage as StartPage
import pages.UploadPage as UploadPage
import pages.ProcessVariables as ProcessVariables
import pages.SetNames as SetNames
import pages.PreviewVariables as PreviewVariables
import pages.GeneratePage as GeneratePage
import pages.TableUploadPage as TableUploadPage
import pages.TableProcessVariables as TableProcessVariables
import pages.TableSetNames as TableSetNames
import pages.Preferences as Preferences

from helpermodules.constants import CURRENT_VERSION, ICON
from helpermodules.constants import settings_dict, default_func
import helpermodules.PreferencesJsonHandler as PreferencesJsonHandler

class JsonTestCaseTracker(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # self.FONTS = FONTS
        

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
        self.preferences_file_path = ""
        self.settings_file_path = ""
        self.reference_arr_for_name_gen = []
        self.current_dir = os.curdir
        self.accepted_data_types = ["int", "str", "bool", "float", "null"]

        self.pages_navigation_history = []

        # Setting UI 
        # Tk.iconbitmap(self, default=ICON)
        Tk.wm_title(self, f"JSON Test Case Tracker {CURRENT_VERSION}")



        # Setting Size of UI
        SCREEN_RATIO = PreferencesJsonHandler.get_data_from_settings("screenRatio")
        if not (0.7 < SCREEN_RATIO < 1):
            SCREEN_RATIO = 0.85 
        Tk.geometry(self, self.get_screen_dimentions(SCREEN_RATIO))
        

        # Global Container
        self.global_container = Frame(self)
        self.global_container.pack(side=TOP, fill=BOTH, expand=True)

        self.global_container.grid_rowconfigure(0, weight=1)
        self.global_container.columnconfigure(0, weight=1)

        FRAMES = [
            StartPage.StartPage,
            UploadPage.UploadPage,
            ProcessVariables.ProcessVariables,
            SetNames.SetNames,
            PreviewVariables.PreviewVariables,
            GeneratePage.GeneratePage,
            TableUploadPage.TableUploadPage,
            TableProcessVariables.TableProcessVariables,
            TableSetNames.TableSetNames,
            Preferences.Preferences
        ]

        for FRAME in FRAMES:
            frame = FRAME(self.global_container, self)
            self.frames[FRAME] = frame
            frame.grid(row=0, column=0, sticky=NSEW)


        # Add Menu
        self.add_menu()

        self.show_frame(StartPage.StartPage)

    def restart(self):
        self.pages_navigation_history = []
        self.show_frame(StartPage.StartPage)


    def show_frame(self, FrameName):
        frame = self.frames[FrameName]
        self.pages_navigation_history.append(frame)
        frame.tkraise()

    def go_back(self):
        self.pages_navigation_history.pop()
        prev_frame = self.pages_navigation_history[len(self.pages_navigation_history) - 1]
        prev_frame.tkraise()

    def get_screen_dimentions(self, ratio:float = 0.8):
        
        ScreenSizeX = self.winfo_screenwidth()
        ScreenSizeY = self.winfo_screenheight()
        ScreenRatio = ratio
        FrameSizeX  = int(ScreenSizeX * ScreenRatio)
        FrameSizeY  = int(ScreenSizeY * ScreenRatio)
        FramePosX   = int((ScreenSizeX - FrameSizeX)/2)
        FramePosY   = int((ScreenSizeY - FrameSizeY)/2)
        
        return f"{FrameSizeX}x{FrameSizeY}+{FramePosX}+{FramePosY}"

    def add_menu(self):
        menu = Menu(self)
        self.config(menu=menu)

        # File Menu
        file_menu = Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Edit Preferences", command=self.goto_preferences)
        file_menu.add_command(label="Quit", command=self.quit)

    def goto_preferences(self):
        PreferencesJsonHandler.add_settings_json_file()
        self.show_frame(Preferences.Preferences)


if __name__=='__main__':

    app = JsonTestCaseTracker()
    app.mainloop()