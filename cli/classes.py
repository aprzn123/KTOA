from datetime import datetime
import logging

# Manages tasks.
class Task(object):
    def __init__(self, name, due, importance, timetotake, char, user):
        self.name = name
        self.due = due
        self.importance = importance
        self.timetotake = timetotake
        self.char = char
        self.pomodoros = []
        self.metadata = {
            'created': datetime.now(),
            'updated': datetime.now(),
            'creator': user,
            'updator': user,
        }
        logging.info(f'New task object {name} created with char {self.char} due {due} with importance level {importance}')

# A board is a collection of tasks. While it should not be necessary, it is possible to have multiple.
class Board(object):
    def __init__(self, name, tasks, user):
        self.name = name
        self.tasks = tasks
        self.metadata = {
            'created': datetime.now(),
            'updated': datetime.now(),
            'creator': user,
            'updator': user,
        }
        tmp = ', '.join(tasks) if len(tasks) > 0 else 'None'
        logging.info(f'Board {name} initialized with tasks {tmp}')

    def new_task(self, char, task, user):
        try:
            self.tasks[char]
        except:
            self.tasks[char] = task
        else:
            print('There is already a task with that char')
            logging.warning('Cannot create a new task when '
                            'there is already a task with the same char')
        self.metadata['updated'] = datetime.now()
        self.metadata['updator'] = user

    def disp(self):
        pass
        print()

class DataManager(object):
    boards = {}
    focus = False
    saved = True
    funcs = []
    bin_key = {
        'start_meta': 65535,
        'end_meta': 65534,
    }
    def __init__(self, username):
        self.username = username