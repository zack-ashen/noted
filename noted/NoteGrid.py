"""Helper functions for printing out grid of notes.json or one note. These functions
assist with the printing of a grid of notes.json. Primarily manipulate a nested list
object which can be ragged or note.

Author: Zachary Ashen
Date: June 4th 2020
"""

import os
import re
from textwrap import fill
from . import NotedItem


# get terminal dimensions
columns, rows = os.get_terminal_size()
width = columns


def _listify_noted_item(noted_item_list):
    # Returns: a ragged list of notes with the format [[['list title'],['list body']], [['list title'],['item 1']]]
    # Precondition: noted_item_list is a list of NotedItem objects.
    note_list_formatted = []

    for index in range(len(noted_item_list)):
        note = noted_item_list[index]
        note_title = note.title
        # execute if note is a list
        if type(note) == NotedItem.ListItem:
            # Only retrieve unchecked list items
            note_list = note.get_unchecked_items()
            note_list.insert(0, note_title)
            note_list_formatted.append(note_list)
        # execute if note is a note not list
        elif type(note) == NotedItem.NoteItem:
            note_list = note.body_text.rstrip('\n').split('\n')
            note_list.insert(0, note_title)
            note_list_formatted.append(note_list)
    return note_list_formatted


def _wrap_text(nested_list):
    # Returns: a nested list with return keys if the string within the nested list goes beyond the width of the
    # terminal.
    # Precondition: nested_list is a ragged list of NotedItem objects that has already been listified using
    # _listify_noted_item.
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


def _add_list_border(nested_list):
    # Returns: a ragged list with ASCII borders. The nested lists will have borders.
    # Precondition: list is a nested list and all items in the nested list are strings
    for index in range(len(nested_list)):
        list_item = nested_list[index]
        border_width = max(len(s) for s in list_item)

        # add top border
        top_border = ['┌' + '─' * border_width + '┐']
        top_border = re.sub("['',]", '', str(top_border)).strip('[]')
        nested_list[index].insert(0, top_border)

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
        nested_list[index].append(bottom_border)
    return nested_list


def _remove_list_border(nested_list):
    # Returns: a ragged list without ASCII borders the returned list will not have any borders.
    # Precondition: nested_list contains borders applied to it by the function _add_list_borders and nested_list is a
    # ragged list.
    for index in range(len(nested_list)):
        nested_list[index].pop(0)
        nested_list[index].pop(len(nested_list[index]) - 1)

    for index in range(len(nested_list)):
        for i in range(len(nested_list[index])):
            nested_list[index][i] = re.sub("[│□]", '', str(nested_list[index][i])).rstrip(' ').lstrip(' ')
    return nested_list


def _build_note_list(noted_item_list):
    # Returns: a formatted note list with borders and in list format for an easier way to display in grid view.
    # Precondition: noted_item_list is a list of NotedItem objects.
    noteList = _add_list_border(_wrap_text(_listify_noted_item(noted_item_list)))
    return noteList


def print_grid(noted_item_list, start_pos=0):
    """ Prints out a grid of NotedItem objects with borders and responsively to the size of the terminal.
    @param noted_item_list: is a list of NotedItem objects.
    @param start_pos: the position in the array of NotedItem objects to begin printing. This should be left alone and
    the default value of 0 should be used. As the function is recursively called this is increased to print more rows.
    """
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
