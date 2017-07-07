import os

from bs4 import BeautifulSoup
from enum import Enum

count_iteration = None


class Element(object):
    def __init__(self, location_element, title_element, text_element):
        self.location_ele = location_element
        self.title_ele = title_element
        self.text_ele = text_element

    def get_title(self):
        return self.title_ele

    def get_location(self):
        return self.location_ele

    def get_text(self):
        return self.text_ele

    def check_is_class(self):
        if self.title_ele == Title.CLAZZ:
            return True

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


def check_title(title):
    del title[-1]
    for t in title:
        if t is not None:
            parsed_title = str(t)
            if "." in parsed_title:
                parsed_title = parsed_title.split(".", 1)[0]
            if "-" in parsed_title:
                parsed_title = parsed_title.split("-", 1)[0]
            for e in Title:
                if e.value in parsed_title:
                    return e


def check_member(member):
    return True


def check_for_class(current_iteration, entry):
    i = int(0)
    first_class = str()
    first_name = str()
    first_class_location = str()
    first_class_found = int(0)

    if entry.check_is_class():
        first_class_found = 1
        if count_iteration is not None:
            count_iteration[i] = current_iteration

        first_class = entry.get_title()
        first_class_location = entry.get_location()
        first_name = entry.get_text()

        if first_class_found == 1 and first_class is not None and first_class_location is not None:
            if entry.get_title() in first_class:
                if entry.get_location() == first_class_location:
                    print "first name", first_name
                    print "first class", first_class
                    print "first location", first_class_location

    location_entry = entry.get_location()
    xyz = location_entry[location_entry.find("(")+1:location_entry.find(")")]
    i +=1

    print xyz, entry.get_text, entry.get_title


    # return [xyz, entry.get_text(), entry.get_title() ]


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

        if text_element is not None:
            new_title = check_title(title_element)
            if location_element is None:
                text_location_element = text_element.parent.attrs
                element_list.append(Element(text_location_element, new_title, text_element.text))
            else:
                element_list.append(Element(location_element, new_title, text_element.text))

    current_iteration = int(0)
    count_iteration = [(len(element_list))]

    for xy in element_list:
        current_iteration += 1
        vaules = check_for_class( current_iteration, xy )


        xy.print_element()


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
