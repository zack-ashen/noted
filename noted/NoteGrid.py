"""Helper functions for printing out grid of notes or one note. These functions \
assist with the printing of a grid of notes. Primarily manipulate a nested list
object which can be ragged or note.

Author: Zachary Ashen
Date: June 4th 2020
"""

import os
import re
from textwrap import fill

import NotedItem


columns, rows = os.get_terminal_size()
width = columns

def _listifyNotedItem(notedItemList):
    """Returns: a nested list from a Google Note object. Checked items are removed from the list.

    Example: Google Note object with list titled 'Foo List' and items:
    'get apples', "pick up groceries" and a note titled 'Foo Note' with text:
    'Garbage in garbage out the end of this note', becomes:
    [[["Foo List"], ["get apples"], ["pick up gorceries"]],
    [["Foo Note"], ["Garbage in garbage out"], ["the end of this note"]]

    Precondition: googleNote is a list containing either items of type
    'gkeepapi.node.List' or 'gkeepapi.node.Note'"""


    # This is the list accumulator that recieves the parsed Google Notes
    noteListFormatted = []

    for index in range(len(notedItemList)):
        note = notedItemList[index]
        noteTitle = note.title
        # execute if note is a list
        if type(note) == NotedItem.ListItem:
            # Only retrieve unchecked list items
            noteList = note.getUncheckedItems()
            noteList.insert(0, noteTitle)
            noteListFormatted.append(noteList)
        # execute if note is a note not list
        elif type(note) == NotedItem.NoteItem:
            noteList = note.bodyText.rstrip('\n').split('\n')
            noteList.insert(0, noteTitle)
            noteListFormatted.append(noteList)
    return noteListFormatted


def _wrapText(nestedList):
    for index in range(len(nestedList)):
        for i in range(len(nestedList[index])):
            if len(nestedList[index][i]) > (width-25):

                nestedList[index][i] = fill(nestedList[index][i], width=(width-22))

                unwrappedText = nestedList[index][i]

                #nestedList[index][i][width-30:width-20].split(' ')
                wrappedTextList = nestedList[index][i].split('\n')
                #print(wrappedTextList)
                for a in range(len(wrappedTextList)):
                    nestedList[index].insert(i+(a), wrappedTextList[a])
                nestedList[index].remove(str(unwrappedText))

    return nestedList


def _addListBorder(nestedList):
    """Returns: a ragged list with ASCII borders. The nested lists will have borders.
    Precondition: list is a nested list and all items in the nested list are strings"""
    for index in range(len(nestedList)):
        listItem = nestedList[index]
        borderWidth = max(len(s) for s in listItem)

        # add top border
        topBorder = ['┌' + '─' * borderWidth + '┐']
        topBorder = re.sub("['',]", '', str(topBorder)).strip('[]')
        nestedList[index].insert(0, topBorder)

        # iterate over middle lines and add border there
        for i in range(len(listItem)):
            if i == 1:
                listItem[i] = '│' + (' ' * ((borderWidth-len(listItem[i]))//2)) + (listItem[i] + ' ' * ((1+borderWidth-len(listItem[i]))//2))[:borderWidth] + '│'
            elif i >= 2:
                listItem[i] = '│' + (listItem[i] + ' ' * borderWidth)[:borderWidth] + '│'

        # add bottom border
        bottomBorder = ['└' + '─' * borderWidth + '┘']
        bottomBorder = re.sub("['',]", '', str(bottomBorder)).strip('[]')
        nestedList[index].append(bottomBorder)
    return nestedList


def _removeListBorder(nestedList):
    for index in range(len(nestedList)):
        nestedList[index].pop(0)
        nestedList[index].pop(len(nestedList[index])-1)

    for index in range(len(nestedList)):
        for i in range(len(nestedList[index])):
            nestedList[index][i] = re.sub("[│□]", '', str(nestedList[index][i])).rstrip(' ').lstrip(' ')
    return nestedList

def _buildNoteList(notedItemList):
    """
    """
    noteList = _addListBorder(_wrapText(_listifyNotedItem(notedItemList)))
    return noteList

def printGrid(notedItemList, startPos=0):
    noteList = _buildNoteList(notedItemList)
    maxNoteListLength = max(len(i) for i in noteList)
    noteListItemWidthAccumulator = 0
    foundColumnCount = False

    global columnEndPos
    global continuePrintingRow

    rowPosition = range(len(noteList))

    # ------ Find columnEndPos ------
    for index in rowPosition[startPos:]:
        noteListItem = noteList[index]

        noteWidth = max(len(s) for s in noteListItem)
        noteListItemWidthAccumulator += noteWidth
        if noteListItemWidthAccumulator > (width-20) and not foundColumnCount:
            columnEndPos = (noteList.index(noteList[index-1]))
            foundColumnCount = True
        elif index == max(rowPosition[startPos:]) and not foundColumnCount and noteListItemWidthAccumulator < width:
            columnEndPos = len(noteList)
            continuePrintingRow = False
            foundColumnCount = True
    # ------ End Find columnEndPos ------

    # ------ Add spaces below note to make rectangular row of characters ------
    if columnEndPos == startPos:
        maxNoteListLength = len(noteList[columnEndPos])
    elif columnEndPos == len(noteList):
        maxNoteListLength = max(len(i) for i in noteList[startPos:columnEndPos])
    else:
        maxNoteListLength = max(len(i) for i in noteList[startPos:columnEndPos+1])

    for index in rowPosition[startPos:columnEndPos+1]:
        noteListItem = noteList[index]
        noteWidth = max(len(s) for s in noteListItem)
        for i in range(len(noteListItem)):
            if len(noteListItem) < maxNoteListLength:
                for x in range(maxNoteListLength-len(noteListItem)):
                    noteListItem.append(' ' * noteWidth)
    # ------ End add spaces below note to make rectangular row of characters ------


    if (columnEndPos+1) == startPos:
        noteListFormatted = noteList[columnEndPos+1]
    else:
        noteListRow = noteList[startPos:columnEndPos+1]

        noteListFormatted = zip(*noteListRow)

        noteListFormatted = list(noteListFormatted)

    # ------ Center Notes ------
    centerSpaceCount = round(abs((width - len(''.join(noteListFormatted[0])))/2))

    for i in range(len(noteListFormatted)):
        print('\u001b[0;33m', end='')
        if i == 1:
            print('\u001b[1;33m', end='')
        stringLine = ''.join(noteListFormatted[i])
        print((centerSpaceCount * ' '), stringLine)

    while continuePrintingRow:
        printGrid(noteList, columnEndPos+1)
