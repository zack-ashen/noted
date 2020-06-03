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

#store terminal width
columns, rows = os.get_terminal_size(0)
width = columns

#noteDict --> noteList --> format

def save(noteList):
    noteFile = open('note_data/notes', 'w')
    #TODO: turn noteList into noteDict
    json.dump(noteFile, noteDict)


def retrieveNotes():
    noteFile = open('note_data/notes', 'r')
    noteDict = json.load(noteFile)
    #TODO convert noteDict into noteList
    noteList = []
    noteFile.close()
    return noteList


def makeAList():
    pass


def makeANote():
    createNoteOptions = [
    {
        'type':'input'
        'input':'What is the title of your note?'
    }]


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
        makeANote()
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
