import logging
import re
from datetime import timedelta, date, datetime

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


# Manages tasks.
class Task(object):
    def __init__(self, name, due, importance, timetotake, char):
        self.name = name
        self.due = due
        self.importance = importance
        self.timetotake = timetotake
        self.char = char
        self.pomodoros = []
        self.metadata = {
            'created'
        }
        logging.info(f'New task object {name} created with char {self.char} due {due} with importance level {importance}')

# A board is a collection of tasks. While it should not be necessary, it is possible to have multiple.
class Board(object):
    def __init__(self, name, tasks):
        self.name = name
        self.tasks = tasks
        self.metadata = {
            'created' = datetime.now(),
            'updated' = datetime.now(),
        }
        tmp = ', '.join(tasks) if len(tasks) > 0 else 'None'
        logging.info(f'Board {name} initialized with tasks {tmp}')

    def new_task(self, char, task):
        try:
            self.tasks[char]
        except: 
            self.tasks[char] = task
        else:
            print('There is already a task with that char')
            logging.warning('Cannot create a new task when '
                            'there is already a task with the same char')
        self.metdata[updated] = datetime.now()

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
    tmp = {
        'name': match.group('func_name'),
        'args': [i.strip(' ') for i in match.group('args').split(',')],
    }
    if len(tmp['args']) == 1 and tmp['args'][0] == '':
        tmp['args'] = []
    return tmp

data = DataManager()

#!  ______________________________________________________  !#
#! \                                                      \ !#
#! |================Here are the functions================| !#
#! \=====They run the commands that the user executes=====\ !#
#! |______________________________________________________| !#

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
        data.boards[name] = Board(name, {})
        print(f'Board {name} created.')
        data.saved = False
    else:
        print('There is already a board with this name.')
        logging.warning(f'NEW_BOARD attempted with already-existing board')
NEW_BOARD.docs = """Creates a new board. 
1 argument:
Name - name of the board"""
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
FOCUS.docs = """Focuses on a board so you can reference the board without
mentioning it in future commands (e.g. add a task to the board without
mentioning the name of the board).
1 argument:
Board - name of the board to focus on"""
data.funcs.append(FOCUS)


def UNFOCUS(args, data):
    data.focus = False
UNFOCUS.docs = """cancels the focusing on a board.
0 arguments"""
data.funcs.append(UNFOCUS)


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

    data.boards[focus].new_task(char, Task(
                                        name_,
                                        due,
                                        importance,
                                        timetotake,
                                        char
    ))
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
data.funcs.append(ADD_TASK)


def LIST_BOARDS(args, data):
    for board in data.boards:
        print(board)
    print()
LIST_BOARDS.docs = """"""
data.funcs.append(LIST_BOARDS)


def SAVE(args, data): # TODO: Make SAVE do stuff.
    pass
SAVE.docs = """"""
data.funcs.append(SAVE)


def HELP(args, data):
    print('\nHELP:\n')
    #TODO: write function docs.
    for func in data.funcs:
        print(func.__name__, end=':\n')
        print(func.docs, end='\n\n')
HELP.docs = """"""
data.funcs.append(ADD_TASK)


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
        SAVE(args, data)

    elif name == 'ADD_TASK':
        ADD_TASK(args, data)

    elif name == 'LIST_BOARDS':
        LIST_BOARDS(args, data)

    elif name == 'HELP':
        HELP(args, data)
