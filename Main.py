import os
import re
import pdb

from bs4 import BeautifulSoup
from enum import Enum

count_iteration = None
relations_list = []
class_to_build = []


class ClassToBuild(object):
    def __init__(self, class_type, class_name, class_variables, class_constructors, class_methods):
        self.class_type = class_type
        self.class_name = class_name
        self.class_variables = class_variables
        self.class_methods = class_methods
        self.class_constructors = class_constructors


class Attribute(object):
    def __init__(self, attribute_access_type, attribute_type, attribute_name):
        self.attribute_name = attribute_name
        self.attribute_type = attribute_type
        self.attribute_access_type = attribute_access_type

    def print_attribute(self):
        return ("ACCESS TYPE: %s \n\t\tRETURN TYPE: %s \n\t\tNAME: %s\n" % (
            self.attribute_access_type, self.attribute_type, self.attribute_name))


class Method(object):
    def __init__(self, method_access_type, method_type, method_name, method_arguments):
        self.method_type = method_type
        self.method_access_type = method_access_type
        self.method_arguments = method_arguments
        self.method_name = method_name

    def print_method(self):
        if self.method_arguments is not None:
            return ("ACCESS TYPE: %s \n\t\tRETURN TYPE: %s \n\t\tNAME: %s\n\t\tARGUMENTS: %s\n" % (
                self.method_access_type, self.method_type, self.method_name, self.method_arguments))
        else:
            return ("ACCESS TYPE: %s \n\t\tRETURN TYPE: %s \n\t\tNAME: %s\n\t\tARGUMENTS: None\n" % (
                self.method_access_type, self.method_type, self.method_name))


class Constructor(object):
    def __init__(self, constructor_access_type, constructor_name, constructor_arguments):
        self.constructor_access_type = constructor_access_type
        self.constructor_name = constructor_name
        self.constructor_arguments = constructor_arguments

    def print_constructor(self):
        return ("ACCESS TYPE: %s \n\t\tNAME: %s \n\t\tARGUMENTS: %s\n" % (
            self.constructor_access_type, self.constructor_name, self.constructor_arguments))


class ClassMember(object):
    def __init__(self, class_name, class_member_type, class_member_value):
        self.class_name = class_name
        self.class_member_type = class_member_type
        self.class_member_value = class_member_value

    def __init__(self, class_type, class_name, class_member_type, class_member_value):
        self.class_type = class_type
        self.class_name = class_name
        self.class_member_type = class_member_type
        self.class_member_value = class_member_value

    def print_class_member(self):
        print("CLASS NAME: %s \n\tCLASS MEMBER VALUE: %s \n\tCLASS MEMBER TYPE: %s\n" % (
            self.class_name, self.class_member_value, self.class_member_type))


class Relation(object):
    def __init__(self, location, value, type):
        self.location = location
        self.value = value
        self.type = type

    def __eq__(self, other):
        return self.type == other.type

    def __hash__(self):
        return hash(self.type)


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


class AccessType(Enum):
    PUBLIC = "+"
    PROTECTED = "#"
    PRIVATE = "-"


class CollectionType(Enum):
    ARRAY = "["
    LIST = "List<"
    MAP = "Map<"


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


def check_member(members):
    class_member = members.class_name
    class_method = members.class_member_value
    str_array = members.class_member_value.split("\\(")[0].split(" ")
    class_name = str()

    if len(str_array) >= 2:
        class_name = str_array[1]
    else:
        class_name = str_array[0]

    if "(" in class_method and ")" in class_method and str(class_member).startswith(class_name):
        members.class_member_type = Title.CONSTRUCTOR
    elif "(" in class_method and ")" in class_method:
        members.class_member_type = Title.METHOD
    else:
        members.class_member_type = Title.VARIABLE


def arrange_method_variables():
    class_list = []
    dict_list = []

    for relation in relations_list:
        class_type = relation.type
        class_details = [relation.value, relation.type]

        if class_type == Title.CLAZZ or class_type == Title.INTERFACE or class_type == Title.ENUM:
            temp_class_dict = (relation.location, [class_details[0], class_details[1]])
            dict_list.append(temp_class_dict)

    for entry in dict_list:
        temp_class = []
        for r in relations_list:
            class_type = r.type

            if class_type != Title.CLAZZ:
                if class_type != Title.INTERFACE:
                    if class_type != Title.ENUM:
                        member_location = float(r.location)
                        class_location = float(entry[0])
                        f = class_location - member_location
                        if f <= 0:
                            if f <= -10:
                                continue
                            else:
                                # class_type, class_name, class_member_type, class_member_value
                                temp_class.append(ClassMember(entry[1][1], entry[1][0], r.type, r.value))

        class_list.append(temp_class)

    return class_list


def check_for_class(current_iteration, entry):
    i = int(0)

    if entry.check_is_class():
        if count_iteration is not None:
            count_iteration[i] = current_iteration

    location_entry = str(entry.get_location())
    xyz = re.search('\(([^)]+)', location_entry)
    if xyz is None:
        xyz = "0.0"
    else:
        xyz = xyz.group(1)
    i += 1

    return [str(xyz).split(",")[0], str(entry.get_text()), entry.get_title()]


def parse_variable(class_members):
    variable_list = []
    access_type = str()
    variable_name = str()
    return_type = str()

    for c in class_members:
        if c.class_member_type != Title.CONSTRUCTOR and c.class_member_type != Title.METHOD:
            if c.class_member_type == Title.VARIABLE:
                class_value = c.class_member_value

                if " " not in class_value:
                    variable_name = class_value
                    access_type = ""
                    return_type = ""
                else:
                    variable_name = parse_variable_name(class_value)
                    access_type = parse_access_type(class_value)
                    return_type = parse_variable_return_type(class_value)

                if access_type is not None and variable_name is not None and return_type is not None:
                    variable_list.append(Attribute(access_type, return_type, variable_name))

    return variable_list


def parse_name(cv):
    for l in str(cv).splitlines():
        foo = l.split("(", 1)[0]
        new_line = foo.translate(None, "+-#")
        return new_line.strip()


def parse_arguments(cv):
    cv_str = str(cv)
    new_str = cv_str[cv_str.find("(")+1:cv_str.find(")")]
    args = re.search("[a-zA-Z]", new_str).string
    args_dict = {}

    if "," in cv:
        new_f = args.split(",")
        for a_new_f in new_f:
            f2 = a_new_f.split(":")
            args_dict[str(f2[0]).strip()] = str(f2[1]).strip()
    else:
        if args is not None:
            f2 = args.split(":")
            args_dict[str(f2[0]).strip()] = str(f2[1]).strip()

    return args_dict


def check_for_arguments(cv):
    cv_str = str(cv)
    new_str = cv_str[cv_str.find("(")+1:cv_str.find(")")]
    are_args = re.search("[a-zA-Z]", new_str)
    return are_args


def parse_access_type(cv):
    access_type = str(cv)[0:1]

    if access_type == AccessType.PUBLIC.value:
        return "public"
    elif access_type == AccessType.PROTECTED.value:
        return "protected"
    elif access_type == AccessType.PRIVATE.value:
        return "private"
    else:
        return "public"


def parse_variable_name(cv):
    return str(cv).split(" ")[1]


def parse_variable_return_type(cv):
    if CollectionType.LIST.value in cv or CollectionType.MAP.value in cv:
        return str(cv).split(":")[1]
    else:
        return str(cv).split(" ")[3]


def parse_constructor(constructor):
    constructor_list = []
    new_arg_dict = dict
    access_type = str()
    constructor_name = str()

    for cm in constructor:
        if cm.class_member_type == Title.METHOD:
            if cm.class_member_type == Title.VARIABLE:
                class_value = cm.class_member_value

                if check_for_arguments(class_value) is not None:
                    new_arg_dict = parse_arguments(class_value)

                constructor_name = parse_name(class_value)
                access_type = parse_access_type(class_value)

                if access_type is not None and constructor_name is not None:
                    if new_arg_dict is not None:
                        constructor_list.append(Constructor(access_type, constructor_name, new_arg_dict))
                    else:
                        constructor_list.append(Constructor(access_type, constructor_name))

    return constructor_list


def parse_method(method):
    method_list = []
    access_type = str()
    method_name = str()
    return_type = str()

    for cm in method:
        new_arg_dict = {}

        if cm.class_member_type != Title.CONSTRUCTOR:
            if cm.class_member_type != Title.VARIABLE:
                class_value = cm.class_member_value

                if check_for_arguments(class_value) is not None:
                    new_arg_dict = parse_arguments(class_value)

                method_name = parse_name(class_value)
                access_type = parse_access_type(class_value)

                if check_for_arguments(class_value) is not None:
                    return_type = parse_argument_method_return_type(class_value)
                else:
                    return_type = parse_method_return_type(class_value)

                if access_type is not None and method_name is not None and return_type is not None:
                    if len(new_arg_dict) != 0:
                        method_list.append(Method(access_type, return_type, method_name, new_arg_dict))
                    else:
                        method_list.append(Method(access_type, return_type, method_name, None))

    return method_list


def parse_argument_method_return_type(cv):
    index = int(str(cv).rfind(":"))
    if index != -1:
        foo = str(cv)[index:].split(" ")
        return foo[1]
    return None


def parse_method_return_type(cv):
    foo = str(cv).split(":")
    return foo[1]


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
                translate = location_element.attrs["transform"]
                if "0" in translate:
                    new_class_location = location_element.parent.attrs
                    element_list.append(Element(new_class_location, new_title, text_element.text))

    current_iteration = int(0)

    for xy in element_list:
        current_iteration += 1
        va = check_for_class(current_iteration, xy)
        relations_list.append(Relation(va[0], va[1], va[2]))

    class_map = arrange_method_variables()

    for class_members in class_map:
        for temp_object in class_members:
            check_member(temp_object)

        variables = parse_variable(class_members)
        methods = parse_method(class_members)
        constructor = parse_constructor(class_members)
        clazz = ClassToBuild(class_members[0].class_member_type, class_members[0].class_name, variables, constructor, methods)
        class_to_build.append(clazz)

    output_classes(class_to_build)


def output_classes(class_list):
    for cl in class_list:
        print cl.class_name

        print "\tVariables"
        class_attributes = cl.class_variables
        for ca in class_attributes:
            print "\t\t" + ca.print_attribute()

        print "\tMethods"
        class_methods = cl.class_methods
        for cm in class_methods:
            print "\t\t" + cm.print_method()


if __name__ == '__main__':
    current_dir = os.getcwd()

    file_path_list = list()

    for root, dirs, files in os.walk(os.getcwd()):
        for f in files:
            if f.endswith(".svg"):
                file_path_list.append(os.path.join(root, f))

    for file_path in file_path_list:
        with open(file_path) as f:
            line_list = f.readlines()
            line_list = [x.strip() for x in line_list]
            begin_conversion(line_list)
