import os

MYSH_PATH = os.path.dirname(os.path.abspath(__file__))

variables = {
    'PS': '$'
}

loop_is_running = True

cwd_history = [os.getcwd()]

def get_variable(name):
    if name in variables:
        return variables[name]

    return ''

def get_process_builtin_path(name):
    return os.path.join(MYSH_PATH, 'process_builtins', name + '.py')
