"""Noted Items class and subclasses including Notes Class and Lists Class.

Author: Zachary Ashen
Date: June 4th 2020
"""


class _NotedItem(object):
    def __init__(self, title):
        self.title = title


class NoteItem(_NotedItem):
    def __init__(self, title, body_text):
        super().__init__(title)
        self.body_text = body_text

    def to_dict(self):
        list_item_dict = {
            'title': self.title,
            'body': self.body_text
        }
        return list_item_dict


class ListItem(_NotedItem):
    def __init__(self, title, *items):
        super().__init__(title)
        self.items = items

    def get_unchecked_items(self):
        unchecked_list = []
        for item in self.items[0]:
            if not item[1]:
                unchecked_list.append('□ ' + item[0])
        return unchecked_list

    def add_item(self, item):
        self.items[0].append(item)

    def delete_item(self, item_name):
        for item in self.items[0]:
            if item_name == item[0]:
                print(self.items[0])
                index_of_item = self.items[0].index(item)
                self.items[0].pop(index_of_item)

    def rename_item(self, old_name, new_name):
        for item in self.items[0]:
            if old_name == item[0]:
                item_list = list(item)
                item_list[0] = new_name
                index_of_item = self.items[0].index(item)
                self.items[0][index_of_item] = tuple(item_list)

    def check_item(self, items_to_check):
        for item in self.items[0]:
            for item_to_check in items_to_check:
                if item[0] == item_to_check:
                    index_of_item = self.items[0].index(item)
                    item_list = list(item)
                    item_list[1] = True
                    item = tuple(item_list)
                    self.items[0][index_of_item] = item

    def to_dict(self):
        list_item_dict = {
            'title': self.title,
            'items': self.items
        }

        return list_item_dict
