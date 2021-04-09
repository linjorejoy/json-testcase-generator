from tkinter import Tk, ttk, Frame


"""

my_notebook.select(get_data_frame)
"""


def main():
    root = Tk()
    root.title("JSON Testcase Creator v0.0.1")
    root.geometry("1000x650")

    # Notebook
    my_notebook = ttk.Notebook(master=root)
    my_notebook.pack(pady="6")


    # Get Data Frame
    get_data_frame = Frame(my_notebook, width=800, height=650)
    



    # Process Data Frame

    process_data_frame = Frame(my_notebook, width=1000, height=650)


    # Preview Outputs Frame


    preview_data_frame = Frame(my_notebook, width=1000, height=650)



    # Generate Status Frame

    generate_data_frame = Frame(my_notebook, width=1000, height=650)




    # Pack Frames
    get_data_frame.pack(fill="both", expand=1)
    process_data_frame.pack(fill="both", expand=1)
    preview_data_frame.pack(fill="both", expand=1)
    generate_data_frame.pack(fill="both", expand=1)

    # adding tabs

    my_notebook.add(get_data_frame, text="Get Data")
    my_notebook.add(process_data_frame, text="Process Data")
    my_notebook.add(preview_data_frame, text="Preview Data")
    my_notebook.add(generate_data_frame, text="Generate Data")

    root.mainloop()



if __name__ == '__main__':
    main()

