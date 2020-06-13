"""Noted Items class and subclasses including Notes Class and Lists Class.

Author: Zachary Ashen
Date: June 4th 2020
"""

import re


class _NotedItem(object):
    """
    """
    def __init__(self, title):
        self.title = title


class NoteItem(_NotedItem):
    """
    """
    def __init__(self, title, bodyText):
        super().__init__(title)
        self.bodyText = bodyText

    def toDict(self):
        listItemDict = {
            'title': self.title,
            'body': self.bodyText
        }
        return listItemDict


class ListItem(_NotedItem):
    def __init__(self, title, *items):
        super().__init__(title)
        self.items = items
        self._itemDict = self._initItemDict()

    def _initItemDict(self):
        itemDict = {}
        for item in self.items:
            itemDict.update({item[0] : item[1]})
        return itemDict

    def getUncheckedItems(self):
        uncheckedList = []
        for item in self.items[0]:
            if not item[1]:
                uncheckedList.append('□ ' + item[0])
        return uncheckedList

    def add_item(self, item):
        pass

    def delete_item(self, item_name):
        for item in self.items[0]:
            if item_name == item[0]:
                print(self.items[0] )
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

    def toDict(self):
        listItemDict = {
            'title' : self.title,
            'items' : self.items
        }

        return listItemDict
