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

    def addBorder(self):
        pass

    def removeBorder(self):
        for index in range(len(nestedList)):
            nestedList[index].pop(0)
            nestedList[index].pop(len(nestedList[index])-1)

        for index in range(len(nestedList)):
            for i in range(len(nestedList[index])):
                nestedList[index][i] = re.sub("[│□]", '', str(nestedList[index][i])).rstrip(' ').lstrip(' ')
        return nestedList


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
