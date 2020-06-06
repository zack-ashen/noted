"""Helper functions for printing out grid of notes. These functions assist with
the printing of a grid of notes. Primarily manipulate a nested list object which
can be ragged or note.

Author: Zachary Ashen
Date: June 4th 2020
"""

from textwrap import fill
import NotedItem

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


def removeListBorder(nestedList):
    for index in range(len(nestedList)):
        nestedList[index].pop(0)
        nestedList[index].pop(len(nestedList[index])-1)

    for index in range(len(nestedList)):
        for i in range(len(nestedList[index])):
            nestedList[index][i] = re.sub("[│□]", '', str(nestedList[index][i])).rstrip(' ').lstrip(' ')
    return nestedList


def printGrid(nestedList, startPos=0):
    maxNestedListLength = max(len(i) for i in nestedList)
    nestedListItemWidthAccumulator = 0
    foundColumnCount = False

    global columnEndPos
    global continuePrintingRow

    rowPosition = range(len(nestedList))

    # ------ Find columnEndPos ------
    for index in rowPosition[startPos:]:
        nestedListItem = nestedList[index]

        noteWidth = max(len(s) for s in nestedListItem)
        nestedListItemWidthAccumulator += noteWidth
        if nestedListItemWidthAccumulator > (width-20) and not foundColumnCount:
            columnEndPos = (nestedList.index(nestedList[index-1]))
            foundColumnCount = True
        elif index == max(rowPosition[startPos:]) and not foundColumnCount and nestedListItemWidthAccumulator < width:
            columnEndPos = len(nestedList)
            continuePrintingRow = False
            foundColumnCount = True
    # ------ End Find columnEndPos ------

    # ------ Add spaces below note to make rectangular row of characters ------
    if columnEndPos == startPos:
        maxNestedListLength = len(nestedList[columnEndPos])
    elif columnEndPos == len(nestedList):
        maxNestedListLength = max(len(i) for i in nestedList[startPos:columnEndPos])
    else:
        maxNestedListLength = max(len(i) for i in nestedList[startPos:columnEndPos+1])

    for index in rowPosition[startPos:columnEndPos+1]:
        nestedListItem = nestedList[index]
        noteWidth = max(len(s) for s in nestedListItem)
        for i in range(len(nestedListItem)):
            if len(nestedListItem) < maxNestedListLength:
                for x in range(maxNestedListLength-len(nestedListItem)):
                    nestedListItem.append(' ' * noteWidth)
    # ------ End add spaces below note to make rectangular row of characters ------


    if (columnEndPos+1) == startPos:
        nestedListFormatted = nestedList[columnEndPos+1]
    else:
        nestedListRow = nestedList[startPos:columnEndPos+1]

        nestedListFormatted = zip(*nestedListRow)

        nestedListFormatted = list(nestedListFormatted)

    # ------ Center Notes ------
    centerSpaceCount = round(abs((width - len(''.join(nestedListFormatted[0])))/2))

    for i in range(len(nestedListFormatted)):
        print('\u001b[0;33m', end='')
        if i == 1:
            print('\u001b[1;33m', end='')
        stringLine = ''.join(nestedListFormatted[i])
        print((centerSpaceCount * ' '), stringLine)

    while continuePrintingRow:
        printGrid(nestedList, columnEndPos+1)
