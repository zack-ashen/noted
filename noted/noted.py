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
import NoteGrid
import NotedItem

#store terminal width
columns, rows = os.get_terminal_size()
width = columns

def saveNotes(noteList):
    noteFile = open('note_data/notes', 'w')
    noteDict = {}
    for notedItemIndex in range(len(noteList)):
        notedItem = noteList[notedItemIndex]
        if type(notedItem) == NotedItem.NoteItem:
            noteDict.update({notedItemIndex : {'title' : notedItem.title, 'body': notedItem.bodyText}})
        elif type(notedItem) == NotedItem.ListItem:
            noteDict.update({notedItemIndex : {'title' : notedItem.title, 'items': notedItem.items}})
    json.dump(noteDict, noteFile)


def retrieveNotes():
    noteFile = open('note_data/notes', 'r')
    noteDict = json.load(noteFile)
    #TODO convert noteDict into noteList
    refreshedNoteList = []
    for notedItem in noteDict:
        noteItemDict = noteDict[notedItem]
        if 'body' in noteItemDict.keys():
            newNoteItem = NotedItem.NoteItem(noteItemDict['title'], noteItemDict['body'])
        elif 'items' in noteItemDict.keys():
            newNoteItem = NotedItem.NoteItem(noteItemDict['title'], noteItemDict['items'])
        refreshedNoteList.append(newNoteItem)
    noteFile.close()
    return refreshedNoteList


def makeAList():
    pass

def makeANote(noteList):
    """Make a ListItem
    """
    noteTitlePrompt = [
    {
        'type': 'input',
        'name': 'noteTitle',
        'message': 'What should the title of the note be?',
    }]

    noteTitleAnswer = prompt(noteTitlePrompt)

    noteTitle = noteTitleAnswer['noteTitle']

    os.system('$EDITOR note')

    with open('note', 'r') as file:
        noteBody = file.read()

    os.system('rm note')

    newNote = NotedItem.NoteItem(noteTitle, noteBody)

    noteList.append(newNote)

    saveNotes(noteList)
    noteView()


def editNoteSelectorView():
    pass


def noteView():
    #attempt to retrieve notes from previous run and print to screen
    try:
        noteList = retrieveNotes()
        NoteGrid.printGrid(noteList)
        options = [
        '✎ Make a New Note ✎',
        '✎ Make a New List ✎',
        '✎ Edit a Note ✎',
        '⛔ Exit ⛔']
    #no previous notes exist so prompt to create a new note or list
    except:
        print('\u001b[1;31m', end='')
        print('You don\'t have any notes!'.center(width))
        options = [
            '✎ Make a New Note ✎',
            '✎ Make a New List ✎',
            '⛔ Exit ⛔'
        ]
        noteList = []

    noteOptions = {
    'type':'list',
    'name':'noteChoice',
    'message':'Please select an option for notes:',
    'choices':options}

    noteOptionsChoice = prompt(noteOptions)

    if noteOptionsChoice['noteChoice'] == '✎ Make a New Note ✎':
        makeANote(noteList)
    elif noteOptionsChoice['noteChoice'] == '✎ Make a New List ✎':
        makeAList()
    elif noteOptionsChoice['noteChoice'] == '✎ Edit a Note ✎':
        editNoteSelectorView()
    elif noteOptionsChoice['noteChoice'] == '⛔ Exit ⛔':
        return

def animateWelcomeText():
    """Animates the welcome noted text in ASCII font and welcome paragraph."""

    fig = Figlet(font='ogre', justify='center', width=width)

    welcomeText = 'noted...'

    print('\u001b[1;34m', end='')

    text = ''
    for character in welcomeText:
        os.system('clear')
        text += character
        print(fig.renderText(text))
        sleep(0.1)

    print('\u001b[0;34m', end='')
    paragraphText = 'Hello! This is a terminal based note taking program. It is still in development so feel free to leave comments or suggestions on the github page: https://github.com/zack-ashen/noted. I tried to add a decent amount of features. However, if there is something you want to see feel free to make a request on github or email: zachary.h.a@gmail.com. Thanks! \n'

    paragraphStrings = []

    if width < 100:
        print(paragraphText)
    else:
        paragraphText = str(fill(paragraphText, width/2))
        paragraphTextList = paragraphText.split('\n')
        for index in range(len(paragraphTextList)):
            print(paragraphTextList[index].center(width))
        print('\n')

        line = ''
        for index in range(width):
            line += '─'
        print(line)


def main():
    animateWelcomeText()
    noteView()


if __name__ == '__main__':
    main()
