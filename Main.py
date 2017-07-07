import os

from bs4 import BeautifulSoup
from enum import Enum


class Element(object):
    def __init__(self, location_element, title_element, text_element):
        self.location_ele = location_element
        self.title_ele = title_element
        self.text_ele = text_element

    def print_element(self):
        print(self.location_ele, self.title_ele, self.text_ele)


class Title(Enum):
    CLAZZ = "Class"
    ENUM = "Enumeration"
    INTERFACE = "Interface"
    MEMBER = "Member"
    PACKAGE = "Package"
    NOTE = "Note"
    PAGE = "Page"
    SHEET = "Sheet"
    INHERITANCE = "Inheritance"
    ASSOCIATION = "Association"
    AGGREGATION = "Aggregation"
    COMPOSITION = "Composition"
    DEPENDENCY = "Dependency"
    DIRECTED_ASSOCIATION = "Directed Association"
    INTERFACE_REALIZATION = "Interface Realization"
    CONSTRUCTOR = "Constructor"
    METHOD = "Method"
    VARIABLE = "Variable"

    def check_input(titl):
        del titl[-1]
        for t in titl:
            if t is not None:
                parsed_title = t.next
                if "." in parsed_title:
                    parsed_title = parsed_title.split(".", 1)[0]
                if "-" in parsed_title:
                    parsed_title = parsed_title.split("-", 1)[0]


def begin_conversion(content_list):
    html_str = str()
    element_list = []

    for cl in content_list:
        html_str += cl

    document = BeautifulSoup(html_str, "html.parser")
    for loc in document.select("[transform*=translate]"):
        location_element = loc.find("g", attrs={"transform": True})
        title_element = loc.find("title")
        text_element = loc.find("text")

        # if location_element is None:
        #     location_element = str(text_element)
        #     print location_element


        if text_element is not None:
            if location_element is None:
                text_location_element = text_element.parent.attrs
                element_list.append(Element(text_location_element, title_element.text, text_element.text))
            else:
                element_list.append(Element(location_element, title_element.text, text_element.text))


    for x in element_list:
        x.print_element()


if __name__ == '__main__':
    current_dir = os.getcwd()

    file_path_list = list()

    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file.endswith(".svg"):
                file_path_list.append(os.path.join(root, file))

    for file_path in file_path_list:
        with open(file_path) as f:
            line_list = f.readlines()
            line_list = [x.strip() for x in line_list]
            begin_conversion(line_list)
