from tkinter import Tk, Frame
from tkinter import BOTH, TOP, NSEW

import os

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

from helpermodules.constants import SCREEN_RATIO, CURRENT_VERSION, ICON


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
        self.reference_arr_for_name_gen = []
        self.current_dir = os.curdir
        self.accepted_data_types = ["int", "str", "bool", "float", "null"]



        # Setting UI 
        # Tk.iconbitmap(self, default=ICON)
        Tk.wm_title(self, f"JSON Test Case Tracker {CURRENT_VERSION}")



        # Setting Size of UI
        Tk.geometry(self, self.get_screen_dimentions(SCREEN_RATIO))
        

        # Global Container
        global_container = Frame(self)
        global_container.pack(side=TOP, fill=BOTH, expand=True)

        global_container.grid_rowconfigure(0, weight=1)
        global_container.columnconfigure(0, weight=1)


        FRAMES = [
            StartPage.StartPage,
            UploadPage.UploadPage,
            ProcessVariables.ProcessVariables,
            SetNames.SetNames,
            PreviewVariables.PreviewVariables,
            GeneratePage.GeneratePage,
            TableUploadPage.TableUploadPage,
            TableProcessVariables.TableProcessVariables,
            TableSetNames.TableSetNames
        ]

        for FRAME in FRAMES:
            frame = FRAME(global_container, self)
            self.frames[FRAME] = frame
            frame.grid(row=0, column=0, sticky=NSEW)


        self.show_frame(StartPage.StartPage)


    def show_frame(self, FrameName):

        frame = self.frames[FrameName]
        frame.tkraise()


    def get_screen_dimentions(self, ratio:float = 0.8):
        
        ScreenSizeX = self.winfo_screenwidth()
        ScreenSizeY = self.winfo_screenheight()
        ScreenRatio = ratio
        FrameSizeX  = int(ScreenSizeX * ScreenRatio)
        FrameSizeY  = int(ScreenSizeY * ScreenRatio)
        FramePosX   = int((ScreenSizeX - FrameSizeX)/2)
        FramePosY   = int((ScreenSizeY - FrameSizeY)/2)
        
        return f"{FrameSizeX}x{FrameSizeY}+{FramePosX}+{FramePosY}"




if __name__=='__main__':

    app = JsonTestCaseTracker()
    app.mainloop()