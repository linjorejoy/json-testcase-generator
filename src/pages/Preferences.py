from tkinter import Frame, LabelFrame, Entry
from tkinter import N, Y, BOTH, SW, SE, W, SUNKEN, END

from widgetclasses.MyLabelFrame import MyLabelFrame
from widgetclasses.MyButton import MyButton
from widgetclasses.MyEntry import MyEntry
from widgetclasses.MyLabel import MyLabel
from widgetclasses.DoubleScrolledFrame import DoubleScrolledFrame

from helpermodules.MyFonts import FONTS


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
        self.setspacesForTabs()
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
            pady=10
        )
        this_entry = MyEntry(
            self.body_scrollable,
            self.controller,
            grid=(row,1),
            padx=10,
            pady=10
        )
        this_entry.insert(END, self.controller.get_data_from_settings('screenRatio'))
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
            pady=10
        )
        this_entry = MyEntry(
            self.body_scrollable,
            self.controller,
            grid=(row,1),
            padx=10,
            pady=10
        )
        this_entry.insert(END, self.controller.get_data_from_settings('fileNameCounterStart'))
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
            pady=10
        )
        this_entry = MyEntry(
            self.body_scrollable,
            self.controller,
            grid=(row,1),
            padx=10,
            pady=10
        )
        this_entry.insert(END, self.controller.get_data_from_settings('reportJsonPrefix'))
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
            pady=10
        )
        this_entry = MyEntry(
            self.body_scrollable,
            self.controller,
            grid=(row,1),
            padx=10,
            pady=10
        )
        this_entry.insert(END, self.controller.get_data_from_settings('spacesForTabs'))
        self.form_entry_obj["spacesForTabs"] = (this_entry, 'int')
        

    def setoverwriteExistingJsonWithSameFileName(self):
        row = self.get_row()
        
        
        MyLabel(
            self.body_scrollable,
            self.controller,
            text="overwriteExistingJsonWithSameFileName",
            font=FONTS['LARGE_FONT_2'],
            grid=(row,0),
            padx=10,
            pady=10
        )
        this_entry = MyEntry(
            self.body_scrollable,
            self.controller,
            grid=(row,1),
            padx=10,
            pady=10
        )
        this_entry.insert(END, self.controller.get_data_from_settings('overwriteExistingJsonWithSameFileName'))
        self.form_entry_obj["overwriteExistingJsonWithSameFileName"] = (this_entry, 'bool')
    

    def setautoAddCounterForGeneratedFiles(self):
        row = self.get_row()
        MyLabel(
            self.body_scrollable,
            self.controller,
            text="autoAddCounterForGeneratedFiles",
            font=FONTS['LARGE_FONT_2'],
            grid=(row,0),
            padx=10,
            pady=10
        )
        this_entry = MyEntry(
            self.body_scrollable,
            self.controller,
            grid=(row,1),
            padx=10,
            pady=10
        )
        this_entry.insert(END, self.controller.get_data_from_settings('autoAddCounterForGeneratedFiles'))
        self.form_entry_obj["autoAddCounterForGeneratedFiles"] = (this_entry, 'bool')
        

    def saveChanges(self):
        new_dict = {}
        for key in self.form_entry_obj.keys():
            entry_cell, datatype = self.form_entry_obj[key]
            new_dict[key] = self.get_data_from_entry(key, entry_cell, datatype)
        self.controller.overwrite_settings_json_file(new_dict)
        self.go_back()
        

    def get_data_from_entry(self, key:str, entry:Entry, datatype:str):

        if datatype == "str":
            return entry.get()

        elif datatype == 'float':
            data = ""
            try:
                data = float(entry.get())
            except ValueError:
                data = self.controller.get_data_from_settings(key)
            return data

        elif datatype == 'int':
            data = ""
            try:
                data = int(float(entry.get()))
            except ValueError:
                data = self.controller.get_data_from_settings(key)
            return data

        elif datatype == 'bool':
            data = ""
            entry_value = entry.get()
            if entry_value in self.true_values:
                data = True
                
            elif entry_value in self.false_values:
                data = False

            else:
                data = self.controller.get_data_from_settings(key)
            return data
            
        else:
            pass


    def set_ui(self):
        pass


    def go_back(self):
        self.controller.go_back()
        