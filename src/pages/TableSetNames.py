from tkinter import Frame, Label
from tkinter import StringVar
from tkinter import N, Y, SW, SE


from widgetclasses.MyLabelFrame import MyLabelFrame
from widgetclasses.MyOptionMenu import MyOptionMenu
from widgetclasses.MyButton import MyButton
from widgetclasses.MyLabel import MyLabel
from widgetclasses.DoubleScrolledFrame import DoubleScrolledFrame
from widgetclasses.MyEntry import MyEntry

from helpermodules.MyFonts import FONTS
import helpermodules.FileNameGenerator as FileNameGenerator


import pages.TableProcessVariables as TableProcessVariables
import pages.PreviewVariables as PreviewVariables
# import pages.PreviewVariables as PreviewVariables

import JSON_Test_Case_Generator


class TableSetNames(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.variables_for_dropdown = ["None", "Counter", "Additional Comment"]
        self.widgets_added = []

        self.header_label_frame = MyLabelFrame(
            self,
            controller,
            text="Info",
            height="50",
            expand=N
        )

        test_label = Label(self.header_label_frame, text="Set Names", font = FONTS["LARGE_FONT"])
        test_label.pack(padx=10, pady=10)

        self.body_label_frame = MyLabelFrame(
            self,
            controller,
            text="Body",
            height="500",
            expand=Y
        )

        self.body_scrollable = DoubleScrolledFrame(self.body_label_frame)

        self.footer_label_frame = MyLabelFrame(
            self,
            controller,
            text="Footer",
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
            text="Preview Results",
            command=self.goto_next,
            rely=1.0,
            relx=1.0,
            x=-5,
            y=-5,
            anchor=SE
        )

    def set_ui(self):
        self.destroy_existing_widgets()
        self.set_widgets()

    def destroy_existing_widgets(self):
        for widget in self.widgets_added:
            widget.destroy()
        self.controller.reference_arr_for_name_gen = []
        self.widgets_added = []

    def set_widgets(self):
        
        self.variables_for_dropdown = ["None", "Counter", "AdditionalComment", *self.controller.VARIABLES_PRESENT]
        entry_0 = MyEntry(
            self.body_scrollable,
            self.controller,
            grid=(0, 0)
        )
        self.widgets_added.append(entry_0)
        self.controller.reference_arr_for_name_gen.append(entry_0)
        for index in range(len(self.variables_for_dropdown)):

            if not self.variables_for_dropdown:
                self.variables_for_dropdown = [""]
            
            plus_label_0 = MyLabel(
                self.body_scrollable,
                self.controller,
                text="+",
                font=FONTS['FONT_PLUS_SIGN'],
                grid=(index, 1)
            )

            this_dropdown_var = StringVar()
            this_dropdown_var.set(None)

            this_dropdown = MyOptionMenu(
                self.body_scrollable,
                self.controller,
                this_dropdown_var,
                options=self.variables_for_dropdown,
                grid=(index, 2),
                padx=1,
                pady=3
            )
            self.controller.reference_arr_for_name_gen.append(this_dropdown_var)
            
            plus_label_1 = MyLabel(
                self.body_scrollable,
                self.controller,
                text="+",
                font=FONTS['FONT_PLUS_SIGN'],
                grid=(index, 3)
            )

            entry_n = MyEntry(
                self.body_scrollable,
                self.controller,
                grid=(index, 4),
                padx=1,
                pady=3
            )
            self.widgets_added.append(plus_label_0)
            self.widgets_added.append(this_dropdown)
            self.widgets_added.append(plus_label_1)
            self.widgets_added.append(entry_n)

            self.controller.reference_arr_for_name_gen.append(entry_n)

        self.body_scrollable.pack(side="top", fill="both", expand=True)

    def goto_next(self):
        self.controller.show_frame(PreviewVariables.PreviewVariables)
        # self.controller.frames[PreviewVariables.PreviewVariables].set_ui()

    def go_back(self):
        self.controller.go_back()