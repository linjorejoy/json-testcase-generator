from typing import List, Any


class EntryCell:
    def __init__(self, key, value, variable_name=None):
        self.variable_name:str
        self.key:Any = key
        self.value: Any = value

    def __hash__(self):
        return hash(self)
    # def __str__(self):
    #     return f"EntryCell : {self.value} \n"

    # def __repr__(self):
    #     return f"EntryCell : {self.value}"

        
        