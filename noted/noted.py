"""
Noted
Author: Zachary Ashen
Date: June 2nd 2020
Description: A CLI note taking app designed to function similarly to Google Keep.
Contact: zachary.h.a@gmail.com
"""

import os
from time import sleep
from textwrap import fill
import json

from pyfiglet import Figlet
from PyInquirer import prompt

from .NoteGrid import print_grid
from . import NotedItem


# get terminal width
width, height = os.get_terminal_size()

# path to stored notes
dir, filename = os.path.split(__file__)
notes_file_path = os.path.join(dir, "note_data", "notes.json")


def save_notes(note_list):
    """Saves notes by converting note_list into a dictionary and storing in a JSON file.
    @param note_list: a list of NotedItem objects to be saved in a file for future use.
    """
    note_dict = {}
    for noted_item_index in range(len(note_list)):
        noted_item = note_list[noted_item_index]
        if type(noted_item) == NotedItem.NoteItem:
            note_dict.update({noted_item_index: {'title': noted_item.title, 'body': noted_item.body_text}})
        elif type(noted_item) == NotedItem.ListItem:
            note_dict.update({noted_item_index: {'title': noted_item.title, 'items': noted_item.items}})

    note_file = open(notes_file_path, 'w')
    json.dump(note_dict, note_file)


def retrieve_notes():
    """Retrieves notes from notes.json file and converts them from a dictionary back into a list of NotedItem objects.
    @return: a list of Noted Item objects both NoteItems and ListItems.
    """
    note_file = open(notes_file_path, 'r')
    note_dict = json.load(note_file)

    refreshed_note_list = []
    for noted_item in note_dict:
        note_item_dict = note_dict[noted_item]
        if 'body' in note_item_dict.keys():
            new_note_item = NotedItem.NoteItem(note_item_dict['title'], note_item_dict['body'])
        elif 'items' in note_item_dict.keys():
            for item in range(len(note_item_dict['items'][0])):
                note_item_dict['items'][0][item] = tuple(note_item_dict['items'][0][item])
            new_note_item = NotedItem.ListItem(note_item_dict['title'], note_item_dict['items'][0])
        refreshed_note_list.append(new_note_item)

    return refreshed_note_list


def change_note_title():
    """Gives a prompt for user to select a title either a new one or changing a previous notes title.
    @return: a string for the notes title.
    """
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

    try:
        note_list = retrieve_notes()
        for item in note_list:
            if note_title == item.title:
                print('Sorry, but you must choose a unique title. You have already used that title...')
                note_title = change_note_title()
    except json.decoder.JSONDecodeError:
        pass
    return note_title


def edit_note_body(previous_text=''):
    """Gives a prompt using the $EDITOR environment variable to create a new note body text either for the first time
    or changing the previous note body.
    @param previous_text: previous text is a string of the previous note_body text if changing the from a previous note.
    If it is a brand new note the default value is used of nothing.
    @return: a string of the new note body text.
    """
    os.system('touch note')

    note_body_file = open('note', "w")
    note_body_file.write(previous_text)
    note_body_file.close()

    os.system('$EDITOR note')

    with open('note', 'r') as file:
        note_body = file.read()

    os.system('rm note')
    return note_body


def make_a_list(note_list, display_note_view=True):
    """Makes a ListItem
    @param note_list: a list of NotedItem objects.
    @param display_note_view: whether to display note_view after creating a NotedList or return.
    """
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
    """Makes a NoteItem
    @param note_list: a list of NotedItem objects.
    @param display_note_view: whether to display note_view after creating a NotedList or return.
    """
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
    """Deletes a note
    @param note_list: a list of NotedItem objects.
    @param index_of_note: the index of the item to delete in the note_list.
    @return: the edited note_list without the item meant to be deleted.
    """
    del note_list[index_of_note]
    return note_list


def edit_note_title(noted_item):
    """Edit the note title
    @param noted_item: a NotedItem object
    @return: a noted_item with a different title.
    """
    noted_item.title = change_note_title()
    return noted_item


def check_items_view(noted_list):
    """A view to check items off a ListItem displays all of the unchecked items and allows the user to select which ones
    to check off.
    @param noted_list: a ListItem object.
    @return: a new noted_list with the edited note having checked off items.
    """
    items = noted_list.get_unchecked_items()

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
    """A view for editing the names of items in a ListItem or deleting items in a ListItem.
    @param noted_list: a ListItem object.
    @param index_of_note: the index of the item to delete in the note_list.
    @return: a new ListItem object with the edited items.
    """
    items = noted_list.get_unchecked_items()

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
    """A view for adding items to a ListItem. Gives a prompt for a series of inputs to continue adding unchecked items.
    @param noted_list: a ListItem object.
    @return: an edited ListItem object with items added.
    """
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
    """Edit the body text of a NoteItem
    @param note: the NoteItem object to change the body text of.
    @return: a new NoteItem object with a different body text.
    """
    new_text = edit_note_body(note.body_text)
    note.body_text = new_text
    return note


def edit_note_view(index_of_note):
    """A view to edit a NotedItem object whether it is a NoteItem or ListItem.
    @param index_of_note: the index of the note to edit in note_list.
    """
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
    """Display a list of notes in notes.json file and have user select which note they want to edit. After selecting the
    note the note gets passed to edit_note_view.
    """
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
    """Display a grid of notes and options to manipulate those notes or create new notes."""
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
    except json.decoder.JSONDecodeError:
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
    """Animate a welcome text display and then display a grid of notes with options to edit or create new notes."""
    animate_welcome_text()
    note_view()


if __name__ == '__main__':
    main()
