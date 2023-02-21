import re
from typing import (List, Tuple)

class MergeMTObject:
    minutes_map = {
        "60": "M1",
        "120": "M2",
        "180": "M3",
        "240": "M4",
        "300": "M5",
        "360": "M6",
        "600": "M10",
        "720": "M12",
        "900": "M15",
        "1200": "M20",
        "1800": "M30",
        "3600": "H1",
        "7200": "H2",
        "10800": "H3",
        "14400": "H4",
        "21600": "H6",
        "28800": "H8",
        "43200": "H12",
        "86400": "D1",
        "604800": "W1",
        "2592000": "MN1"
    }

    content_list1: List[str] = []
    content_list2: List[str] = []
    pattern_indicator = re.compile(r"<indicator>.*</indicator>", re.DOTALL)
    pattern_object = re.compile(r"(<object>.*?</object>)", re.DOTALL)
    output_file_name = "chart_out.chr"
    encoding = "utf-8"

    def __init__(self, encoding, output_file_name):
        self.encoding = encoding
        self.output_file_name = output_file_name

    def strip_line(self, line_str: str) -> List[str]:
        return line_str.strip().split("=")

    def read_input_file(self, input_file: str, order: int) -> Tuple[str, str]:
        if not input_file.endswith("chr"):
            print(f"The file extension of {input_file} is not '.chr'")
            return ("", "")

        try:
            f = open(input_file, 'r', encoding=encoding)
            if order == 1:
                self.content_list1 = f.readlines()
            elif order == 2:
                self.content_list2 = f.readlines()
        except Exception as e:
            print("Open file error:", e)
            return ("", "")
        finally:
            if f:
                f.close()

        data_symbol = self.strip_line(self.content_list1[2])
        data_period = self.strip_line(self.content_list1[3])
        print(f"File{order} is:", data_symbol[1],
              self.minutes_map.get(data_period[1]))

        return (data_symbol[1], data_period[1])

    def find_name_chart_object(self, file_content: str) -> List[str]:
        for i in self.pattern_indicator.findall(file_content):
            if i[12:21] == "name=main":
                return self.pattern_object.findall(i)

    def merge(self, input_file1: str, input_file2: str):
        symbol1, period1 = self.read_input_file(input_file1, 1)
        symbol2, period2 = self.read_input_file(input_file2, 2)

        if symbol1 != symbol2:
            raise ValueError("The symbols in two input files are different!")

        chart2_main_object = self.find_name_chart_object("".join(
            self.content_list2))
        with open(self.output_file_name, "w", encoding=encoding) as f:
            rep = "name=main\n" + "".join(chart2_main_object) + "\n"
            f.write("".join(self.content_list1).replace("name=main\n", rep))


# Variables
encoding = "GB18030"  # Use your own encoding. For simplified Chinese is GB18030.
output_file_name = "chart_out.chr"
input_file_name1 = "chart01.chr"
input_file_name2 = "chart02.chr"

# Merge
m = MergeMTObject(encoding, output_file_name)
m.merge(input_file_name1, input_file_name2)
