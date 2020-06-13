#!/usr/bin/python3
"""
Noted
Author: Zachary Ashen
Date: June 2nd 2020
Description: A CLI note taking app designed to function similarly to Google Keep.
Contact: zachary.h.a@gmail.com
"""

import os
from time import sleep
import re
from pyfiglet import Figlet
from PyInquirer import prompt
from textwrap import fill
import argparse
import json
from NoteGrid import print_grid
import NotedItem

# get terminal width
width, height = os.get_terminal_size()


def save_notes(note_list):
    note_file = open('note_data/notes', 'w')
    note_dict = {}
    for notedItemIndex in range(len(note_list)):
        noted_item = note_list[notedItemIndex]
        if type(noted_item) == NotedItem.NoteItem:
            note_dict.update({notedItemIndex: {'title': noted_item.title, 'body': noted_item.body_text}})
        elif type(noted_item) == NotedItem.ListItem:
            note_dict.update({notedItemIndex: {'title': noted_item.title, 'items': noted_item.items}})
    json.dump(note_dict, note_file)


def retrieve_notes():
    note_file = open('note_data/notes', 'r')
    note_dict = json.load(note_file)

    refreshed_note_list = []
    for notedItem in note_dict:
        note_item_dict = note_dict[notedItem]
        if 'body' in note_item_dict.keys():
            new_note_item = NotedItem.NoteItem(note_item_dict['title'], note_item_dict['body'])
        elif 'items' in note_item_dict.keys():
            for item in range(len(note_item_dict['items'][0])):
                note_item_dict['items'][0][item] = tuple(note_item_dict['items'][0][item])
            new_note_item = NotedItem.ListItem(note_item_dict['title'], note_item_dict['items'][0])
        refreshed_note_list.append(new_note_item)

    note_file.close()

    return refreshed_note_list


def change_note_title():
    note_title_prompt = [
        {
            'type': 'input',
            'name': 'note_title',
            'message': 'What should the title of the note be?',
        }]

    note_title_answer = prompt(note_title_prompt)

    try:
        note_title = note_title_answer['note_title']
    except KeyError:
        return

    note_list = retrieve_notes()
    if note_title in note_list:
        print('Sorry, but you must choose a unique title. You have already used that title...')
        change_note_title()
    return note_title


def edit_note_body(previous_text=''):
    os.system('touch note')

    note_body_file = open('note', "w")
    text_body = note_body_file.write(previous_text)
    note_body_file.close()

    os.system('$EDITOR note')

    with open('note', 'r') as file:
        note_body = file.read()

    os.system('rm note')
    return note_body


def make_a_list(note_list, display_note_view=True):
    note_title = change_note_title()

    list_finished = False
    list_items = []
    while not list_finished:
        add_list_item = [
            {
                'type': 'input',
                'name': 'list_item',
                'message': 'Add a list item (Enter \'-\' to finish):',
            }]

        list_item_answer = prompt(add_list_item)

        try:
            list_item = (list_item_answer['list_item'], False)
        except KeyError:
            return

        list_items.append(list_item)

        if list_item_answer['list_item'] == '-':
            list_items.pop(len(list_items) - 1)
            list_finished = True

    new_list_item = NotedItem.ListItem(note_title, list_items)
    note_list.append(new_list_item)

    save_notes(note_list)

    if display_note_view:
        note_view()
    else:
        return


def make_a_note(note_list, display_note_view=True):
    note_title = change_note_title()

    note_body = edit_note_body()

    new_note = NotedItem.NoteItem(note_title, note_body)

    note_list.append(new_note)

    save_notes(note_list)

    if display_note_view:
        note_view()
    else:
        return


def delete_note(note_list, index_of_note):
    del note_list[index_of_note]
    return note_list


def edit_note_title(noted_item):
    noted_item.title = change_note_title()
    return noted_item


def check_items_view(noted_list):
    items = noted_list.getUncheckedItems()

    items_list = []
    for item in items:
        item = item.lstrip('□ ')
        item_dict = {'name': item}
        items_list.append(item_dict)

    check_items_prompt = {
        'type': 'checkbox',
        'name': 'item_to_check',
        'message': 'Check off the items...',
        'choices': items_list
    }
    items_to_check = prompt(check_items_prompt)

    try:
        noted_list.check_item(items_to_check['item_to_check'])
    except KeyError:
        return
    return noted_list


def edit_items_view(noted_list, index_of_note):
    items = noted_list.getUncheckedItems()

    items_choices = []
    for item in items:
        item = item.lstrip('□ ')
        items_choices.append(item)

    items_choices.append('...Go Back')

    edit_items_prompt = {
        'type': 'list',
        'name': 'edit_items_list',
        'message': 'What item would you like to rename or delete?',
        'choices': items_choices
    }

    edit_items_selection = prompt(edit_items_prompt)

    try:
        if edit_items_selection['edit_items_list'] == '...Go Back':
            edit_note_view(index_of_note)
        else:
            edit_item_input = {
                'type': 'input',
                'name': 'edited_item',
                'message': 'Edit the item (Delete all text to delete...):',
                'default': edit_items_selection['edit_items_list']
            }
            edit_item_prompt = prompt(edit_item_input)

            if edit_item_prompt['edited_item'] == '':
                noted_list.delete_item(edit_items_selection['edit_items_list'])
            else:
                old_text = edit_items_selection['edit_items_list']
                new_text = edit_item_prompt['edited_item']
                noted_list.rename_item(old_text, new_text)
            return noted_list
    except KeyError:
        return


def add_items_view(noted_list):
    list_finished = False
    while not list_finished:
        add_list_item = [
            {
                'type': 'input',
                'name': 'list_item',
                'message': 'Add a list item (Enter \'-\' to finish):',
            }]

        list_item_answer = prompt(add_list_item)

        if list_item_answer['list_item'] == '-':
            list_finished = True
        else:
            list_item = (list_item_answer.get('list_item'), False)
            noted_list.add_item(list_item)
    return noted_list


def edit_note_text_view(note):
    new_text = edit_note_body(note.body_text)
    note.body_text = new_text
    return note


def edit_note_view(index_of_note):
    os.system('clear')

    note_list = retrieve_notes()
    note = note_list[index_of_note]
    print_grid([note])

    if type(note) == NotedItem.NoteItem:
        edit_options = ['Edit Note', 'Edit Title', 'Delete this note', 'Go Back']
    elif type(note) == NotedItem.ListItem:
        edit_options = ['Check Items', 'Edit Title', 'Edit/Delete Items', 'Add Items', 'Delete this note', 'Go Back']

    edit_note_prompt = {
        'type': 'list',
        'name': 'editNoteSelector',
        'message': 'What would you like to do to this note?',
        'choices': edit_options
    }

    edit_note_selection = prompt(edit_note_prompt)

    try:
        if edit_note_selection['editNoteSelector'] == 'Edit Title':
            note = edit_note_title(note)
            note_list[index_of_note] = note
            save_notes(note_list)
            edit_note_view(index_of_note)
        elif edit_note_selection['editNoteSelector'] == 'Delete this note':
            note_list = delete_note(note_list, index_of_note)
            save_notes(note_list)
            # if no more notes left return to main view...else select new note to edit
            if len(note_list) == 0:
                note_view()
            else:
                edit_note_selector()
        elif edit_note_selection['editNoteSelector'] == 'Go Back':
            edit_note_selector()
        elif edit_note_selection['editNoteSelector'] == 'Check Items':
            note = check_items_view(note)
            note_list[index_of_note] = note
            save_notes(note_list)
            edit_note_view(index_of_note)
        elif edit_note_selection['editNoteSelector'] == 'Edit/Delete Items':
            note = edit_items_view(note, index_of_note)
            note_list[index_of_note] = note
            save_notes(note_list)
            edit_note_view(index_of_note)
        elif edit_note_selection['editNoteSelector'] == 'Add Items':
            note = add_items_view(note)
            note_list[index_of_note] = note
            save_notes(note_list)
            edit_note_view(index_of_note)
        elif edit_note_selection['editNoteSelector'] == 'Edit Note':
            note = edit_note_text_view(note)
            note_list[index_of_note] = note
            save_notes(note_list)
            edit_note_view(index_of_note)
    except KeyError:
        save_notes(note_list)


def edit_note_selector():
    note_list = retrieve_notes()

    # append all titles of the notes
    note_choices = []
    for item in note_list:
        note_choices.append(item.title)
    note_choices.append('Go Back')

    # display prompt of all note titles to select which to edit
    note_selector_prompt = {
        'type': 'list',
        'name': 'noteSelector',
        'message': 'Please select a note to edit:',
        'choices': note_choices
    }
    note_selection = prompt(note_selector_prompt)

    try:
        if note_selection['noteSelector'] == 'Go Back':
            note_view()
        else:
            index_of_note = note_choices.index(note_selection['noteSelector'])
            edit_note_view(index_of_note)
    except KeyError:
        save_notes(note_list)


def note_view():
    # attempt to retrieve notes from previous run and print to screen
    os.system('clear')
    try:
        note_list = retrieve_notes()
        print_grid(note_list)
        options = [
            '✎ Make a New Note ✎',
            '✎ Make a New List ✎',
            '✎ Edit a Note ✎',
            '⛔ Exit ⛔']
    # no previous notes exist so prompt to create a new note or list
    except IndexError:
        print('\u001b[1;31m', end='')
        print('You don\'t have any notes!'.center(width))
        options = [
            '✎ Make a New Note ✎',
            '✎ Make a New List ✎',
            '⛔ Exit ⛔'
        ]
        note_list = []

    note_options = {
        'type': 'list',
        'name': 'noteChoice',
        'message': 'Please select an option for notes:',
        'choices': options
    }

    note_options_choice = prompt(note_options)

    try:
        if note_options_choice['noteChoice'] == '✎ Make a New Note ✎':
            make_a_note(note_list)
        elif note_options_choice['noteChoice'] == '✎ Make a New List ✎':
            make_a_list(note_list)
        elif note_options_choice['noteChoice'] == '✎ Edit a Note ✎':
            edit_note_selector()
        elif note_options_choice['noteChoice'] == '⛔ Exit ⛔':
            save_notes(note_list)
    except KeyError:
        save_notes(note_list)


def animate_welcome_text():
    """Animates the welcome noted text in ASCII font and welcome paragraph."""

    fig = Figlet(font='ogre', justify='center', width=width)

    welcome_text = 'noted...'

    print('\u001b[1;34m', end='')

    text = ''
    if height < 40:
        for character in welcome_text:
            os.system('clear')
            text += character
            print('\n' * round(height / 4))
            print(fig.renderText(text))
            sleep(0.1)
        os.system('clear')
    else:
        for character in welcome_text:
            os.system('clear')
            text += character
            print(fig.renderText(text))
            sleep(0.1)

        print('\u001b[0;34m', end='')
        paragraph_text = 'Hello! This is a terminal based note taking program. It is still in development so feel free ' \
                         'to leave comments or suggestions on the github page: https://github.com/zack-ashen/noted. I' \
                         ' tried to add a decent amount of features. However, if there is something you want to see ' \
                         'feel free to make a request on github or email: zachary.h.a@gmail.com. Thanks! \n '

        paragraph_strings = []

        if width < 100:
            print(paragraph_text)
        else:
            paragraph_text = str(fill(paragraph_text, width / 2))
            paragraph_text_list = paragraph_text.split('\n')
            for index in range(len(paragraph_text_list)):
                print(paragraph_text_list[index].center(width))
            print('\n')

            line = ''
            for index in range(width):
                line += '─'
            print(line)


def main():
    animate_welcome_text()
    note_view()


if __name__ == '__main__':
    main()
