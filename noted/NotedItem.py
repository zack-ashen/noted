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
            'title' : self.title,
            'body' : self.bodyText
        }
        return listItemDict

class ListItem(_NotedItem):
    """
    """
    def __init__(self, title, *items):
        super().__init__(title)
        self.items = items
        print(items)
        self._itemDict = self._initItemDict()

    def _initItemDict(self):
        itemDict = {}
        for item in self.items:
            itemDict.update({item[0] : item[1]})
        return itemDict

    def addItem(self, item):
        pass

    def deleteItem(self, item):
        pass

    def checkItem(self, item):
        pass

    def setItem(self, item):
        pass

    def toDict(self):
        listItemDict = {
            'title' : self.title,
            'items' : self.items
        }

        return listItemDict
