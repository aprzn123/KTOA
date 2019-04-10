import logging
import re
from datetime import timedelta, date, datetime

# Separates dev log from standard log.
DEVLOAD = True

print(f'\nCLI program started{" with DEVLOAD " if DEVLOAD else " "}at {datetime.now()}')

if DEVLOAD:
    logging.basicConfig(filename='cli_DEV.log', level=logging.INFO)
else:
    logging.basicConfig(filename='cli.log', level=logging.INFO)
logging.info(f'program started at {datetime.now()}----------------------------------')


# Manages tasks.
class Task(object):
    def __init__(self, name, due, importance, timetotake, char=False):
        self.name = name
        self.due = due
        self.importance = importance
        self.timetotake = timetotake
        if char:
            self.char = char
        else:
            self.char = self.name[0]
        self.pomodoros = []
        logging.info(f'New task object {name} created with char {self.char} due {due} with importance level {importance}')

# A board is a collection of tasks. While it should not be necessary, it is possible to have multiple.
class Board(object):
    def __init__(self, name, tasks):
        self.name = name
        self.tasks = tasks
        tmp = ', '.join(tasks) if len(tasks) > 0 else 'None'
        logging.info(f'Board {name} initialized with tasks {tmp}')

    def disp(self):
        pass
        print()

class DataManager(object):
    boards = {}
    focus = False
    saved = True
    funcs = []

# Regex to parse user input.
choice_regex = re.compile(r'(?P<func_name>[\w_]+)\((?P<args>.*)\)')

def parse_input(input_):
    match = choice_regex.match(input_)
    if match is None:
        return
    return {
        'name': match.group('func_name'),
        'args': match.group('args').split(),
    }

data = DataManager()

#!  ______________________________________________________  !#
#! \                                                      \ !#
#! |                Here are the functions                | !#
#! \     They run the commands that the user executes     \ !#
#! |______________________________________________________| !#

def QUIT(data):
    if data.saved:
        quit()
    else:
        print('are you sure you want to quit? you have unsaved work. (y/n)', end='\n>')
        response = input()
        if response == 'y':
            quit()
QUIT.docs = """"""
data.funcs.append(QUIT)


def NEW_BOARD(args, data):
    if len(args) < 1:
        print('More arguments needed.')
        logging.warning('NEW_BOARD attempted with an insufficient amount of arguments')
        return

    name = args[0]

    try:
        data.boards[name]
    except KeyError:
        data.boards[name] = Board(name, [])
        print(f'Board {name} created.')
        data.saved = False
    else:
        print('There is already a board with this name.')
        logging.warning(f'NEW_BOARD attempted with already-existing board')
NEW_BOARD.docs = """"""
data.funcs.append(NEW_BOARD)


def FOCUS(args, data):
    if len(args) < 1:
        print('More arguments needed.')
        logging.warning('FOCUS attempted with an insufficient amount of arguments')
        return
    if args[0] not in data.boards.keys():
        print('That is not one of your open boards.')
        logging.warning('FOCUS attempted on nonexistent board')
        return
    data.focus = args[0]
FOCUS.docs = """"""
data.funcs.append(FOCUS)


def UNFOCUS(args, data):
    data.focus = False
UNFOCUS.docs = """"""
data.funcs.append(UNFOCUS)


def ADD_TASK(args, data):
    pass
ADD_TASK.docs = """"""
data.funcs.append(ADD_TASK)


def LIST_BOARDS(args, data):
    for board, _ in data.boards:
        print(board)
    print()
LIST_BOARDS.docs = """"""
data.funcs.append(LIST_BOARDS)


def HELP(args, data):
    print('HELP')
    #TODO: access function docs and print those.
    for func in data.funcs:
        print(func.__name__, end=':\n')
        print(func.docs, end='\n\n')
HELP.docs = """"""
data.funcs.append(ADD_TASK)


#!  ______________________________________________________  !#
#! \                                                      \ !#
#! |                 Here is the mainloop                 | !#
#! \______________________________________________________\ !#


while True:
    print('>', end='')
    in_ = input()
    func = parse_input(in_)

    if func is None:
        print('syntax error: unknown')
        logging.warning(f'syntax error: {in_}')
        continue

    name = func['name']
    args = func['args']


    if name == 'QUIT' or name == 'EXIT':
        QUIT(data)

    elif name == 'NEW_BOARD':
        NEW_BOARD(args, data)

    elif name == 'FOCUS':
        FOCUS(args, data)

    elif name == 'UNFOCUS':
        UNFOCUS(args, data)

    elif name == 'ADD_TASK':
        ADD_TASK(args, data)

    elif name == 'SAVE':
        pass # TODO: Create SAVE command

    elif name == 'ADD_TASK':
        ADD_TASK(args, data) # TODO: Set up ADD_TASK command

    elif name == 'LIST_BOARDS':
        LIST_BOARDS(args, data)

    elif name == 'HELP':
        HELP(args, data)
