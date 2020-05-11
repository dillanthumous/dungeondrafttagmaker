# -*- coding: utf-8 -*-
"""
Created on Sun May 10 15:02:03 2020
"""

# Extra container objects for JSON output
from collections import defaultdict
import os
import glob
import json
import PySimpleGUI as sg    

# Gets the current directory as initial default | sets up defaultdict for reasons (https://stackoverflow.com/questions/38799212/python-for-loop-appending-to-every-key-in-dictionary) 
# adds lists for outputs | sets a default value needed for DungeonDraft Folder Structure
base_path = os.curdir
script_location = os.path.realpath(base_path)
imagesList = defaultdict(list)
setsList = []
filePathStruct = "textures/objects/"    

# Theme setter for eye niceness
sg.theme('DarkAmber')
# Basic data entry layout - 1 million times easier than TKinter - inputs are key-value pairs in the "values" dictionary
layout = [
        [sg.Text('Please choose from these optional settings - if you do nothing, the default folder is the script folder, and all other text is blank or defaulted')],
        [sg.Text('Locate the Main Folder that contains your Sub Folders of pngs:'), sg.InputText(), sg.FolderBrowse(key='FOLDER')],
        [sg.Text('Enter a prepended value for your tags (optional):'), sg.InputText(key='PREPEND')],
        [sg.Text('Enter an appended value for your tags (optional):'), sg.InputText(key='APPEND')],
        [sg.Text('Give a custom set name (defaults to "Default Set" - "Colorable" skipped):'), sg.InputText(key='SETNAME')],
        [sg.Submit(), sg.Cancel()]     
]                       
# Window name, setupand reason for being
window = sg.Window('Dungeon Draft Tag Generator - Uses Folder Names to Make Your Tags', layout)    
event, values = window.read() # Capture then inputs    
window.close() # Get rid of window

# Input variable storage - uses keys from a Dict of Key-Value inputs as defined above
base_path = values['FOLDER']
prepend_input = values['PREPEND']
append_input = values['APPEND']   
setname_input = values['SETNAME'] 

# Catch no setnames entered
if setname_input == None:
    setname_input = "Default Set"

# Catch empty folder choices
if base_path == None:
    base_path = os.curdir

# This is the meat and potatoes - attempts to use JSON notation derived from Python Structures (Dict and List) and then uses
# some basic line writing to format it correctly to match the needs of DDraft file - this is VERY fragile and will probably break... :D
def recursive_image_tagging():
    # Recursively collect all files from folders which contain pngs and creates name in a dict
    for file in glob.iglob(os.path.join(base_path, '*/*.png'), recursive=True):
        imagesList[os.path.basename(os.path.dirname(file))].append(filePathStruct + os.path.basename(file))

    # Check for usable user input and call the prepend/append function to add to tag names
    if prepend_input != None or append_input != None:
        prepend_append_to_dict_keys(prepend_input, append_input, imagesList)

    # Creates a list of folders from keys to be returned as the default "Set" for this JSON script
    for k in iter(imagesList):
        if k != "Colorable":
            itemKey = k
            setsList.append(itemKey)
            tagsList = imagesList
        
    # Write the output to a JSON with Indents etc. for niceness - strings for structure and format correctness
    with open('default.dungeondraft_tags', 'w', encoding='utf-8') as f:
        # Strings handle opening and closing lines - dump handles JSON conversion from Python object
        f.write('{\n' + '    "tags" : ')
        json.dump(tagsList, f, ensure_ascii=False, indent=8)
        f.write(',')
        f.write('	\n    "sets" : {\n        ' + '"' + setname_input + '" : ')
        f.write(' ')
        json.dump(setsList, f, ensure_ascii=False, indent=12)
        f.write('\n    }')
        f.write('\n}')
        f.close

# helper function for key swapping in a dict
def keys_swap(orig_key, new_key, d):
    d[new_key] = d.pop(orig_key)

# prepender for dict keys - uses keys_swap
def prepend_append_to_dict_keys(prependage, appendage, d):
    # handles appending
    for each in d.keys():
        if type(d[each]) is dict:
            prepend_append_to_dict_keys(appendage, d[each])
        keys_swap(each, str(each) + appendage, d)
    #  handles prepending
    for each in d.keys():
        if type(d[each]) is dict:
            prepend_append_to_dict_keys(prependage, d[each])
        keys_swap(each, prependage + str(each), d)

# Call the spaghetti script and cross fingers
recursive_image_tagging()

# Tell the player what they have won
print(script_location)
sg.popup('Please check ' + str(script_location) + ' for the output file (if it worked!)')




    

