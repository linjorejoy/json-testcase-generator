from typing import List, Any
from tkinter import Entry

class EntryCell:
    def __init__(self, value: Any=None):
        self.entry:Entry = None
        self.value = value

    def __hash__(self):
        return hash(self)
        
        