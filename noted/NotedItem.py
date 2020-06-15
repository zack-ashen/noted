"""Noted Items class and subclasses including Notes Class and Lists Class.

Author: Zachary Ashen
Date: June 4th 2020
"""


class _NotedItem(object):
    # Master class of NotedItems including NoteItem and ListItem
    # Invariant: title is a string
    def __init__(self, title):
        # Initializes _NotedItem
        # Precondition: title is a string
        self.title = title


class NoteItem(_NotedItem):
    """A note item with a body that can be printed or displayed in a grid format. It is a sticky note type of idea.
    @invariant title: is a string of the title of the note
    @invariant body_text: a string of the text for the body
    """
    def __init__(self, title, body_text):
        """NoteItem initializer
        @param title: is a string of the title of the note
        @param body_text: a string of the text for the body
        """
        super().__init__(title)
        self.body_text = body_text

    def to_dict(self):
        """Converts the NoteItem into a dictionary
        @return: a dictionary with the note item title and body as keys and content
        """
        list_item_dict = {
            'title': self.title,
            'body': self.body_text
        }
        return list_item_dict


class ListItem(_NotedItem):
    """A list of items that can be checked of or displayed in a grid has a format similar to a todo list.
    @invariant title: is a string of the title of the note
    @invariant items: is an item or multiple items with the format of a tuple ('item name', True). The second boolean
    dictates whether the item is checked or not: True means it is checked, False means it is not checked.
    """
    def __init__(self, title, *items):
        """ListItem initializer
        @param title: is a string of the title of the note
        @param items: is an item or multiple items with the format of a tuple ('item name', True). The second boolean
        dictates whether the item is checked or not: True means it is checked, False means it is not checked.
        """
        super().__init__(title)
        self.items = items

    def get_unchecked_items(self):
        """Gets all of the unchecked items in the ListItem
        @return: a list of unchecked items
        """
        unchecked_list = []
        for item in self.items[0]:
            if not item[1]:
                unchecked_list.append('□ ' + item[0])
        return unchecked_list

    def add_item(self, item):
        """Adds item to ListItem
        @param item: tuple of item to add in format ('item name', True) second boolean determines whether the item is
        checked or not if True the item is checked if False the item is not checked.
        """
        self.items[0].append(item)

    def delete_item(self, item_name):
        """Deletes item from ListItem
        @param item_name: string of item name to delete, must be a name of an item
        """
        for item in self.items[0]:
            if item_name == item[0]:
                print(self.items[0])
                index_of_item = self.items[0].index(item)
                self.items[0].pop(index_of_item)

    def rename_item(self, old_name, new_name):
        """Renames an item
        @param old_name: a string of the old name of the item must be in the list item
        @param new_name: a string of the new name of the item
        """
        for item in self.items[0]:
            if old_name == item[0]:
                item_list = list(item)
                item_list[0] = new_name
                index_of_item = self.items[0].index(item)
                self.items[0][index_of_item] = tuple(item_list)

    def check_item(self, items_to_check):
        """Checks items. In other words, converts tuple of item from ('string title', False) to ('string title', True)
        @param items_to_check: is a string of the name of the item to check off
        """
        for item in self.items[0]:
            for item_to_check in items_to_check:
                if item[0] == item_to_check:
                    index_of_item = self.items[0].index(item)
                    item_list = list(item)
                    item_list[1] = True
                    item = tuple(item_list)
                    self.items[0][index_of_item] = item

    def to_dict(self):
        """Converts the ListItem into a dictionary
        @return: a dictionary with the note item title and items as keys and content
        """
        list_item_dict = {
            'title': self.title,
            'items': self.items
        }

        return list_item_dict
