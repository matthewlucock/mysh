import os
import time
import data

# These are the builtins that run in the same process as the shell.

def exit(args):
    data.loop_is_running = False
    print('Goodbye!')

def sleep(args):
    if len(args) == 0:
        print('sleep: missing operand')
        return

    duration = args[0]

    try:
        duration = int(duration)
    except ValueError:
        print('sleep: invalid time interval \'' + duration + '\'')
        return

    time.sleep(duration)

def set(args):
    if len(args) == 0:
        keys = list(data.variables.keys())
        keys.sort(key=str.lower)

        for key in keys:
            print(key + '=' + data.variables[key])

        return

    if len(args) == 1:
        data.variables[args[0]] = ''
        return

    data.variables[args[0]] = ' '.join(args[1:])

def unset(args):
    if len(args) == 0:
        print('unset: missing operand')
        return

    del data.variables[args[0]]

def chdir(path):
    os.chdir(path)
    data.cwd_history.append(os.getcwd())

def changedir(args):
    if len(args) == 0:
        home = data.get_variable('HOME')

        if home:
            chdir(home)

        return

    chdir(args[0])

def historylist(args):
    for index, path in enumerate(reversed(data.cwd_history)):
        print(str(index) + ': ' + path)

def cdn(args):
    if len(args) == 0:
        return

    list_index = len(data.cwd_history) - int(args[0])
    os.chdir(data.cwd_history[list_index])
    data.cwd_history = data.cwd_history[0:list_index]

functions = {
    'exit': exit,
    'sleep': sleep,
    'set': set,
    'unset': unset,
    'changedir': changedir,
    'historylist': historylist,
    'cdn': cdn
}
