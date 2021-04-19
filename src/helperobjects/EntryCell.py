from typing import List, Any
from tkinter import Entry, StringVar

class EntryCell:
    def __init__(self, value: Any=None):
        self.entry:Entry = None
        self.option_value:StringVar = None
        self.value = value

    def __hash__(self):
        return hash(self)
        
        