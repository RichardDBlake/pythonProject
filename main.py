# This is a sample Python script.
from gedcom.parser import Parser
from gedcom.tags import GEDCOM_TAG_OBJECT, GEDCOM_TAG_TITLE, GEDCOM_TAG_FILE, GEDCOM_TAG_FORMAT
from gedcom.element.element import Element
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.
    for i in range(1, 10):
        if (i in [1, 3]):
            print(i)


def create_new_structure(element: Element, structure: str, value: str = "", overwrite: bool = False) -> Element:
    """ Check of an existing structure exists in this element. Create if it does not."""
    if element.get_child_element(structure):
        if overwrite:
            element.get_child_element(structure).set_value(value)
        return element.get_child_element(structure)
    else:
        return element.new_child_element(tag=structure, value=value)

def fix_mft_objects(gedcom_file: Parser) -> None:
    """ Fix Object records from MFT. """
    gedcom_file.invalidate_cache()
    objects = gedcom_file.get_root_child_elements_with_tag(GEDCOM_TAG_OBJECT)
    for this_object in objects:
        for object_elem in this_object.get_child_elements():
            if object_elem.get_tag() == GEDCOM_TAG_TITLE:
                file_structure = create_new_structure(this_object, GEDCOM_TAG_FILE)
                create_new_structure(file_structure, GEDCOM_TAG_TITLE, value=object_elem.get_value(), overwrite=True)
                this_object.get_child_elements().remove(object_elem)
            if object_elem.get_tag() == "URL":
                file_name = object_elem.get_value()
                file_structure = create_new_structure(this_object, GEDCOM_TAG_FILE, value=file_name, overwrite=True)
                create_new_structure(file_structure, GEDCOM_TAG_FORMAT, value="url", overwrite=True)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
