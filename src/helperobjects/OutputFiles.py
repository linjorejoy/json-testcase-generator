from helperobjects.OutputJsonFile import OutputJsonFile

from typing import List

class OutputFiles:

    def __init__(self):
        self.count = 0
        self.output_json_file_array:List[OutputJsonFile] = []

    def add_output_json_file(self, json_file_obj:OutputJsonFile):
        self.count += 1
        self.output_json_file_array.append(json_file_obj)

    def get_output_json_file_array(self):
        return self.output_json_file_array
    
    def clear_output_json_file_arr(self):
        self.count = 0
        self.output_json_file_array = []
    
    def dictionary(self):
        base_dict = {
            "count": self.count,
            "output_json_file_array": [json_file.dictionary() for json_file in self.output_json_file_array]
        }
        return base_dict