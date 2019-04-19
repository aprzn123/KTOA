import logging
import classes
import re
from datetime import date, timedelta
import os

def QUIT(data):
    if data.saved:
        quit()
    else:
        print('are you sure you want to quit? you have unsaved work. (y/n)', end='\n>')
        response = input()
        if response == 'y':
            quit()
QUIT.docs = """Exits the application.
0 arguments"""


def NEW_BOARD(args, data):
    if len(args) < 1:
        print('More arguments needed.')
        logging.warning('NEW_BOARD attempted with an insufficient amount of arguments')
        return

    name = args[0]

    try:
        data.boards[name]
    except KeyError:
        data.boards[name] = classes.Board(name, {}, data.username)
        print(f'Board {name} created.')
        data.saved = False
    else:
        print('There is already a board with this name.')
        logging.warning(f'NEW_BOARD attempted with already-existing board')
NEW_BOARD.docs = """Creates a new board. 
1 argument:
Name - name of the board"""


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
FOCUS.docs = """Focuses on a board so you can reference the board without
mentioning it in future commands (e.g. add a task to the board without
mentioning the name of the board).
1 argument:
Board - name of the board to focus on"""


def UNFOCUS(args, data):
    data.focus = False
UNFOCUS.docs = """cancels the focusing on a board.
0 arguments"""


def ADD_TASK(
            args,
            data,
            datecomp=re.compile(r'(?P<YYYY>\d{4})-(?P<MM>\d{2})-(?P<DD>\d{2})'),
            deltacomp=re.compile(r'(?P<days>\d+)'),
            timecomp=re.compile(r'(?P<HH>\d{2}):(?P<MM>\d{2})')
    ):
    if data.focus:
        argmin = 6
    else:
        argmin = 7
    if len(args) < argmin:
        print('More arguments needed.')
        logging.warning("ADD_TASK attempted with an insufficient amount of arguments")
        return

    due_mode = args[0].lower() == 'direct'
    name_ = args[1]
    due_raw = args[2]
    importance = args[3]
    timetotake_raw = args[4]
    char = args[5]
    if data.focus:
        focus = data.focus
    else:
        focus = args[6]
    if due_mode:
        dcm = datecomp.match(due_raw)
        y = int(dcm.group('YYYY'))
        m = int(dcm.group('MM'))
        d = int(dcm.group('DD'))
        due = date(y, m, d)
    else:
        dcm = deltacomp.match(due_raw)
        tod = date.today()
        interval = timedelta(days=int(dcm.group('days')))
        due = tod + interval

    tcm = timecomp.match(timetotake_raw)
    h = int(tcm.group('HH'))
    m = int(tcm.group('MM'))
    timetotake = timedelta(hours=h, minutes=m)

    data.boards[focus].new_task(
                        char,
                        classes.Task(
                            name_,
                            due,
                            importance,
                            timetotake,
                            char,
                            data.username
                        ),
                        data.username
    )
    saved = False
ADD_TASK.docs = """adds a task to a board (either passed as an argument or focused on)
6 or 7 arguments:
due_mode - whether the due date is direct (give a specific date) or relative (give how
           long until it's due)
name - the name of the task
due - the date it's due (in YYYY-MM-DD format) if you chose direct due mode or how long
      till it's due (just number of days) if you chose relative due mode
importance - a number from 1 to 10: 1 being the least important and 10 being the most important
timetotake - an estimate as to how long an activity will take, in HH:MM format
char - the character used to identify the task in retrieving it from the board
focus (OPTIONAL) - if not focused, determines which board to add the task to"""


def LIST_BOARDS(args, data):
    for board in data.boards:
        print(board)
    print()
LIST_BOARDS.docs = """"""


def SAVE(args, data): # TODO: Make SAVE do stuff.
    pass
SAVE.docs = """"""


def LOAD(args, data):
    if len(args) < 1:
        print('More arguments needed.')
        logging.warning("LOAD attempted with an insufficient amount of arguments")
        return

    if '/' in args[0]:
        path = args[0].split('/')
        path.insert(1, os.sep)
        if path[-1][-5:] not in ('.ktoa', '.ktot'):
            path[-1] += '.ktoa'
        file = os.path.join(*path)

    elif '\\' in args[0]:
        path = args[0].split('\\')
        path.insert(1, os.sep)
        if path[-1][-5:] not in ('.ktoa', '.ktot'):
            path[-1] += '.ktoa'
        file = os.path.join(*path)

    else:
        name = args[0]
        if name[-5:] not in ('.ktoa', '.ktot'):
            name += '.ktoa'
        file = name

    metadata = False

    with open(file, 'rb') as f:
        while  True:
            latest_data = bytes(f.read(2))
            if latest_data == b'':
                break
            value = int.from_bytes(latest_data, byteorder='big')
            if value == data.bin_key['start_meta']:
                metatdata = True
                continue
            if value == data.bin_key['end_meta']:
                metadata = False
                continue

            if metadata:
                pass # TODO: manage metadata (after metadata branch done)
LOAD.docs = """"""


def HELP(args, data):
    print('\nHELP:\n')
    #TODO: write function docs.
    for func in data.funcs:
        print(func.__name__, end=':\n')
        print(func.docs, end='\n\n')
HELP.docs = """"""