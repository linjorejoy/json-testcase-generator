from tkinter import Frame, LabelFrame, Entry, StringVar
from tkinter import N, Y, BOTH, SW, SE, E, W, SUNKEN, END

from widgetclasses.MyLabelFrame import MyLabelFrame
from widgetclasses.MyButton import MyButton
from widgetclasses.MyEntry import MyEntry
from widgetclasses.MyLabel import MyLabel
from widgetclasses.MyOptionMenu import MyOptionMenu
from widgetclasses.DoubleScrolledFrame import DoubleScrolledFrame

from helpermodules.MyFonts import FONTS
from helpermodules.constants import reportJsonTypes, boolTypes
import helpermodules.PreferencesJsonHandler as PreferencesJsonHandler


class Preferences(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.row_count = 0
        self.form_entry_obj = {}
        self.true_values = ["true", "t"]
        self.false_values = ["false", "f"]
        
        self.header_label_frame = MyLabelFrame(
            self,
            self.controller,
            text="Preferences",
            height="80",
            expand=N
        )


        self.body_label_frame = MyLabelFrame(
            self,
            self.controller,
            text="Options",
            height="500",
            expand=True
        )

        self.body_scrollable = DoubleScrolledFrame(self.body_label_frame)
        self.body_scrollable.pack(side="top", fill="both", expand=True)
        
        
        self.setForm()
        


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
            text="Close Preferences",
            command=self.go_back,
            rely=1,
            relx=0,
            x=5,
            y=-5,
            anchor=SW
        )
        

        button_save = MyButton(
            self.footer_label_frame,
            controller,
            text="Save",
            command=self.saveChanges,
            rely=1.0,
            relx=1.0,
            x=-5,
            y=-5,
            anchor=SE
        )

    def get_row(self):
        self.row_count += 1
        return self.row_count

    def setForm(self):
        self.setscreenRatio()
        self.setfileNameCounterStart()
        self.setreportJsonPrefix()
        self.setReportJsonType()
        self.setspacesForTabs()
        self.setadditionalCommentEntryWidth()
        self.setoverwriteExistingJsonWithSameFileName()
        self.setautoAddCounterForGeneratedFiles()


    def setscreenRatio(self):
        row = self.get_row()
        
        MyLabel(
            self.body_scrollable,
            self.controller,
            text="screenRatio",
            font=FONTS['LARGE_FONT_2'],
            grid=(row,0),
            padx=10,
            pady=10,
            sticky=E
        )
        this_entry = MyEntry(
            self.body_scrollable,
            self.controller,
            grid=(row,1),
            padx=10,
            pady=10
        )
        
        MyLabel(
            self.body_scrollable,
            self.controller,
            text="This will define the size of the Application Window (Range: 0.7-1)",
            font=FONTS['LARGE_FONT'],
            grid=(row,3),
            padx=10,
            pady=10,
            sticky=W
        )
        this_entry.insert(END, PreferencesJsonHandler.get_data_from_settings('screenRatio'))
        self.form_entry_obj["screenRatio"] = (this_entry, "float")
        
    
    def setfileNameCounterStart(self):
        row = self.get_row()
        
        MyLabel(
            self.body_scrollable,
            self.controller,
            text="fileNameCounterStart",
            font=FONTS['LARGE_FONT_2'],
            grid=(row,0),
            padx=10,
            pady=10,
            sticky=E
        )
        this_entry = MyEntry(
            self.body_scrollable,
            self.controller,
            grid=(row,1),
            padx=10,
            pady=10
        )
        
        MyLabel(
            self.body_scrollable,
            self.controller,
            text="Where should the counter while naming files start. (Example : 1)",
            font=FONTS['LARGE_FONT'],
            grid=(row,3),
            padx=10,
            pady=10,
            sticky=W
        )
        this_entry.insert(END, PreferencesJsonHandler.get_data_from_settings('fileNameCounterStart'))
        self.form_entry_obj["fileNameCounterStart"] = (this_entry, 'int')

    
    def setreportJsonPrefix(self):
        row = self.get_row()
        
        MyLabel(
            self.body_scrollable,
            self.controller,
            text="reportJsonPrefix",
            font=FONTS['LARGE_FONT_2'],
            grid=(row,0),
            padx=10,
            pady=10,
            sticky=E
        )
        this_entry = MyEntry(
            self.body_scrollable,
            self.controller,
            grid=(row,1),
            padx=10,
            pady=10
        )
        
        MyLabel(
            self.body_scrollable,
            self.controller,
            text="This will be the prefix of the JSON Report file( Example : Report)",
            font=FONTS['LARGE_FONT'],
            grid=(row,3),
            padx=10,
            pady=10,
            sticky=W
        )
        this_entry.insert(END, PreferencesJsonHandler.get_data_from_settings('reportJsonPrefix'))
        self.form_entry_obj["reportJsonPrefix"] = (this_entry, 'str')
        
    
    def setspacesForTabs(self):
        row = self.get_row()
        
        MyLabel(
            self.body_scrollable,
            self.controller,
            text="spacesForTabs",
            font=FONTS['LARGE_FONT_2'],
            grid=(row,0),
            padx=10,
            pady=10,
            sticky=E
        )
        this_entry = MyEntry(
            self.body_scrollable,
            self.controller,
            grid=(row,1),
            padx=10,
            pady=10
        )
        
        MyLabel(
            self.body_scrollable,
            self.controller,
            text="Number of Spaces as an indent while creating json Outputs (Example: 2)",
            font=FONTS['LARGE_FONT'],
            grid=(row,3),
            padx=10,
            pady=10,
            sticky=W
        )
        this_entry.insert(END, PreferencesJsonHandler.get_data_from_settings('spacesForTabs'))
        self.form_entry_obj["spacesForTabs"] = (this_entry, 'int')
    

    def setadditionalCommentEntryWidth(self):
        row = self.get_row()
        
        MyLabel(
            self.body_scrollable,
            self.controller,
            text="additionalCommentEntryWidth",
            font=FONTS['LARGE_FONT_2'],
            grid=(row,0),
            padx=10,
            pady=10,
            sticky=E
        )
        this_entry = MyEntry(
            self.body_scrollable,
            self.controller,
            grid=(row,1),
            padx=10,
            pady=10
        )
        
        MyLabel(
            self.body_scrollable,
            self.controller,
            text="Width of additional Comment(Example : 50, 75, 100)",
            font=FONTS['LARGE_FONT'],
            grid=(row,3),
            padx=10,
            pady=10,
            sticky=W
        )
        this_entry.insert(END, PreferencesJsonHandler.get_data_from_settings('additionalCommentEntryWidth'))
        self.form_entry_obj["additionalCommentEntryWidth"] = (this_entry, 'int')
        

    def setoverwriteExistingJsonWithSameFileName(self):
        row = self.get_row()
        
        
        MyLabel(
            self.body_scrollable,
            self.controller,
            text="overwriteExistingJsonWithSameFileName",
            font=FONTS['LARGE_FONT_2'],
            grid=(row,0),
            padx=10,
            pady=10,
            sticky=E
        )
        this_option_var = StringVar()
        this_option_var.set(str(PreferencesJsonHandler.get_data_from_settings('overwriteExistingJsonWithSameFileName')))

        this_option = MyOptionMenu(
            self.body_scrollable,
            self.controller,
            this_option_var,
            options=boolTypes,
            grid=(row, 1),
            pady=10,
            padx=10
        )
        
        MyLabel(
            self.body_scrollable,
            self.controller,
            text="Keep it true if the existing files in the output folder needs to be overwritten",
            font=FONTS['LARGE_FONT'],
            grid=(row,3),
            padx=10,
            pady=10,
            sticky=W
        )
        self.form_entry_obj["overwriteExistingJsonWithSameFileName"] = (this_option_var, 'options')
    

    def setautoAddCounterForGeneratedFiles(self):
        row = self.get_row()
        MyLabel(
            self.body_scrollable,
            self.controller,
            text="autoAddCounterForGeneratedFiles",
            font=FONTS['LARGE_FONT_2'],
            grid=(row,0),
            padx=10,
            pady=10,
            sticky=E
        )
        this_option_var = StringVar()
        this_option_var.set(str(PreferencesJsonHandler.get_data_from_settings('autoAddCounterForGeneratedFiles')))

        this_option = MyOptionMenu(
            self.body_scrollable,
            self.controller,
            this_option_var,
            options=boolTypes,
            grid=(row, 1),
            pady=10,
            padx=10
        )
        
        MyLabel(
            self.body_scrollable,
            self.controller,
            text="True if Counter is needed. If Counter is not provided. It will add a counter Automatically",
            font=FONTS['LARGE_FONT'],
            grid=(row,3),
            padx=10,
            pady=10,
            sticky=W
        )
        self.form_entry_obj["autoAddCounterForGeneratedFiles"] = (this_option_var, 'options')
        

    def setReportJsonType(self):
        row = self.get_row()
        MyLabel(
            self.body_scrollable,
            self.controller,
            text="reportJsonType",
            font=FONTS['LARGE_FONT_2'],
            grid=(row,0),
            padx=10,
            pady=10,
            sticky=E
        )
        this_option_var = StringVar()
        this_option_var.set(str(PreferencesJsonHandler.get_data_from_settings('reportJsonType')))

        this_option = MyOptionMenu(
            self.body_scrollable,
            self.controller,
            this_option_var,
            options=reportJsonTypes,
            grid=(row, 1),
            pady=10,
            padx=10
        )

        
        MyLabel(
            self.body_scrollable,
            self.controller,
            text="How Detailed do you want your report file to be(Example : choose From Dropdown)",
            font=FONTS['LARGE_FONT'],
            grid=(row,3),
            padx=10,
            pady=10,
            sticky=W
        )

        self.form_entry_obj["reportJsonType"] = (this_option_var, 'options')


    def saveChanges(self):
        new_dict = {}
        for key in self.form_entry_obj.keys():
            entry_cell, datatype = self.form_entry_obj[key]
            new_dict[key] = self.get_data_from_entry(key, entry_cell, datatype)
        
        PreferencesJsonHandler.overwrite_settings_json_file(new_dict)
        self.go_back()
        

    def get_data_from_entry(self, key:str, entry:Entry, datatype:str):

        if datatype == "str":
            return entry.get()

        elif datatype == 'float':
            data = ""
            try:
                data = float(entry.get())
            except ValueError:
                data = PreferencesJsonHandler.get_data_from_settings(key)
            return data

        elif datatype == 'int':
            data = ""
            try:
                data = int(float(entry.get()))
            except ValueError:
                data = PreferencesJsonHandler.get_data_from_settings(key)
            return data

        elif datatype == 'bool':
            data = ""
            entry_value = str(entry.get()).lower()
            if entry_value in self.true_values:
                data = True
                
            elif entry_value in self.false_values:
                data = False

            else:
                data = PreferencesJsonHandler.get_data_from_settings(key)
            return data
        elif datatype == "options":
            return entry.get()
        else:
            pass


    def set_ui(self):
        self.set_values()

    def set_values(self):
        for key in self.form_entry_obj.keys():
            this_entry, data_type = self.form_entry_obj[key]
            if isinstance(this_entry, Entry):
                this_entry.delete(0, END)
                this_entry.insert(END, str(PreferencesJsonHandler.get_data_from_settings(key)))
            elif isinstance(this_entry, StringVar):
                this_entry.set(str(PreferencesJsonHandler.get_data_from_settings(key)))
                


    def go_back(self):
        self.controller.go_back()
        