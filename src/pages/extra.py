


# class StartPage2(Frame):

#     def __init__(self, parent, controller:JsonTestCaseTracker):
#         Frame.__init__(self, parent)
#         self.parent = parent
#         self.controller = controller

#         self.subframe = MyLabelFrame(
#             self,
#             controller,
#             text="Main",
#             height="500",
#             expand=Y
#         )

#         self.subframe_scrollable = DoubleScrolledFrame(self.subframe)
#         for j in range(10):
#             for i in range(20):
#                 EntryWithType(
#                     self.subframe_scrollable,
#                     controller,
#                     frame_name=f"{i} {j} ",
#                     options=["int", "str", "bool", "float"],
#                     grid=(i, j)
#                 )
            
#         self.subframe_scrollable.pack(side="top", fill="both", expand=True)

#         test_label = Label(self, text="Page 0 : Hello World", font = FONTS["LARGE_FONT"])
#         test_label.pack(padx=10, pady=10)

#         button1 = Button(
#             self,
#             text="Goto Page 1",
#             command=lambda:controller.show_frame(UploadPage)
#         )
#         button1.pack(pady=10, padx=10)
    
#     def set_ui(self):
#         pass