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


def _listify_noted_item(noted_item_list):
    # Returns: a nested list from a Google Note object. Checked items are removed from the list.
    #
    # Example: Google Note object with list titled 'Foo List' and items:
    # 'get apples', "pick up groceries" and a note titled 'Foo Note' with text:
    # 'Garbage in garbage out the end of this note', becomes:
    # [[["Foo List"], ["get apples"], ["pick up gorceries"]],
    # [["Foo Note"], ["Garbage in garbage out"], ["the end of this note"]]
    #
    # Precondition: googleNote is a list containing either items of type
    # 'gkeepapi.node.List' or 'gkeepapi.node.Note'

    # This is the list accumulator that recieves the parsed Google Notes
    note_list_formatted = []

    for index in range(len(noted_item_list)):
        note = noted_item_list[index]
        note_title = note.title
        # execute if note is a list
        if type(note) == NotedItem.ListItem:
            # Only retrieve unchecked list items
            note_list = note.getUncheckedItems()
            note_list.insert(0, note_title)
            note_list_formatted.append(note_list)
        # execute if note is a note not list
        elif type(note) == NotedItem.NoteItem:
            note_list = note.bodyText.rstrip('\n').split('\n')
            note_list.insert(0, note_title)
            note_list_formatted.append(note_list)
    return note_list_formatted


def _wrap_text(nested_list):
    for index in range(len(nested_list)):
        for i in range(len(nested_list[index])):
            if len(nested_list[index][i]) > (width - 25):

                nested_list[index][i] = fill(nested_list[index][i], width=(width - 22))

                unwrapped_text = nested_list[index][i]
                wrapped_text_list = nested_list[index][i].split('\n')

                for a in range(len(wrapped_text_list)):
                    nested_list[index].insert(i + (a), wrapped_text_list[a])
                nested_list[index].remove(str(unwrapped_text))

    return nested_list


def _add_list_border(nestedList):
    # Returns: a ragged list with ASCII borders. The nested lists will have borders.
    # Precondition: list is a nested list and all items in the nested list are strings
    for index in range(len(nestedList)):
        list_item = nestedList[index]
        border_width = max(len(s) for s in list_item)

        # add top border
        top_border = ['┌' + '─' * border_width + '┐']
        top_border = re.sub("['',]", '', str(top_border)).strip('[]')
        nestedList[index].insert(0, top_border)

        # iterate over middle lines and add border there
        for i in range(len(list_item)):
            if i == 1:
                list_item[i] = '│' + (' ' * ((border_width - len(list_item[i])) // 2)) + (list_item[i] + ' ' * (
                            (1 + border_width - len(list_item[i])) // 2))[:border_width] + '│'
            elif i >= 2:
                list_item[i] = '│' + (list_item[i] + ' ' * border_width)[:border_width] + '│'

        # add bottom border
        bottom_border = ['└' + '─' * border_width + '┘']
        bottom_border = re.sub("['',]", '', str(bottom_border)).strip('[]')
        nestedList[index].append(bottom_border)
    return nestedList


def _remove_list_border(nested_list):
    for index in range(len(nested_list)):
        nested_list[index].pop(0)
        nested_list[index].pop(len(nested_list[index]) - 1)

    for index in range(len(nested_list)):
        for i in range(len(nested_list[index])):
            nested_list[index][i] = re.sub("[│□]", '', str(nested_list[index][i])).rstrip(' ').lstrip(' ')
    return nested_list


def _build_note_list(noted_item_list):
    noteList = _add_list_border(_wrap_text(_listify_noted_item(noted_item_list)))
    return noteList


def print_grid(noted_item_list, start_pos=0):
    note_list = _build_note_list(noted_item_list)
    max_note_list_length = max(len(i) for i in note_list)
    note_list_item_width_accumulator = 0
    found_column_count = False

    global columnEndPos
    global continuePrintingRow

    row_position = range(len(note_list))

    # ------ Find columnEndPos ------
    for index in row_position[start_pos:]:
        note_list_item = note_list[index]

        note_width = max(len(s) for s in note_list_item)
        note_list_item_width_accumulator += note_width
        if note_list_item_width_accumulator > (width - 20) and not found_column_count:
            columnEndPos = (note_list.index(note_list[index - 1]))
            found_column_count = True
        elif index == max(row_position[start_pos:]) and not found_column_count and note_list_item_width_accumulator < width:
            columnEndPos = len(note_list)
            continuePrintingRow = False
            found_column_count = True
    # ------ End Find columnEndPos ------

    # ------ Add spaces below note to make rectangular row of characters ------
    if columnEndPos == start_pos:
        max_note_list_length = len(note_list[columnEndPos])
    elif columnEndPos == len(note_list):
        max_note_list_length = max(len(i) for i in note_list[start_pos:columnEndPos])
    else:
        max_note_list_length = max(len(i) for i in note_list[start_pos:columnEndPos + 1])

    for index in row_position[start_pos:columnEndPos + 1]:
        note_list_item = note_list[index]
        note_width = max(len(s) for s in note_list_item)
        for i in range(len(note_list_item)):
            if len(note_list_item) < max_note_list_length:
                for x in range(max_note_list_length - len(note_list_item)):
                    note_list_item.append(' ' * note_width)
    # ------ End add spaces below note to make rectangular row of characters ------

    if (columnEndPos + 1) == start_pos:
        note_list_formatted = note_list[columnEndPos + 1]
    else:
        note_list_row = note_list[start_pos:columnEndPos + 1]

        note_list_formatted = zip(*note_list_row)

        note_list_formatted = list(note_list_formatted)

    # ------ Center Notes ------
    center_space_count = round(abs((width - len(''.join(note_list_formatted[0]))) / 2))

    for i in range(len(note_list_formatted)):
        print('\u001b[0;34m', end='')
        if i == 1:
            print('\u001b[1;34m', end='')
        string_line = ''.join(note_list_formatted[i])
        print((center_space_count * ' '), string_line)

    while continuePrintingRow:
        print_grid(note_list, columnEndPos + 1)
