import logging
import os
import re
from datetime import timedelta, date, datetime

import classes
import funcs

print('Enter your name:', end=' ')
username = input()

# Separates dev log from standard log.
DEVLOAD = True

print(f'\nCLI program started{" with DEVLOAD " if DEVLOAD else " "}at {datetime.now()}')

if DEVLOAD:
    logging.basicConfig(filename='cli_DEV.log', level=logging.INFO)
else:
    logging.basicConfig(filename='cli.log', level=logging.INFO)
logging.info(f'program started at {datetime.now()}----------------------------------')


# Regex to parse user input.
choice_regex = re.compile(r'(?P<func_name>[\w_]+)\((?P<args>.*)\)')

def parse_input(input_):
    match = choice_regex.match(input_)
    if match is None:
        return
    tmp = {
        'name': match.group('func_name'),
        'args': [i.strip(' ') for i in match.group('args').split(',')],
    }
    if len(tmp['args']) == 1 and tmp['args'][0] == '':
        tmp['args'] = []
    return tmp

data = classes.DataManager(username)

#!  ______________________________________________________  !#
#! \                                                      \ !#
#! |================Here are the functions================| !#
#! \=====They run the commands that the user executes=====\ !#
#! |______________________________________________________| !#

data.funcs.append(funcs.QUIT)
data.funcs.append(funcs.NEW_BOARD)
data.funcs.append(funcs.FOCUS)
data.funcs.append(funcs.UNFOCUS)
data.funcs.append(funcs.ADD_TASK)
data.funcs.append(funcs.LIST_BOARDS)
data.funcs.append(funcs.SAVE)
data.funcs.append(funcs.LOAD)
data.funcs.append(funcs.ADD_TASK)


#!  ______________________________________________________  !#
#! \                                                      \ !#
#! |=================Here is the mainloop=================| !#
#! \______________________________________________________\ !#


while True:
    print('>', end='')
    in_ = input()
    func = parse_input(in_)

    if func is None:
        print('syntax error: unknown')
        logging.warning(f'syntax error: {in_}')
        continue

    name = func['name'].upper()
    args = func['args']


    if name == 'QUIT' or name == 'EXIT':
        funcs.QUIT(data)

    elif name == 'NEW_BOARD':
        funcs.NEW_BOARD(args, data)

    elif name == 'FOCUS':
        funcs.FOCUS(args, data)

    elif name == 'UNFOCUS':
        funcs.UNFOCUS(args, data)

    elif name == 'ADD_TASK':
        funcs.ADD_TASK(args, data)

    elif name == 'SAVE':
        funcs.SAVE(args, data)

    elif name == 'ADD_TASK':
        funcs.ADD_TASK(args, data)

    elif name == 'LIST_BOARDS':
        funcs.LIST_BOARDS(args, data)

    elif name == 'HELP':
        funcs.HELP(args, data)

    elif name == 'LOAD':
        funcs.LOAD(args, data)
