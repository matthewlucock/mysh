import os
import sys
import data
import re
from command import Command

# This function implements the parser of shell commands.
def interpret_input(shell_input):
    # Normalize whitespace.
    shell_input = re.sub('\t', ' ', shell_input)
    shell_input = re.sub(' +', ' ', shell_input)

    # Just the words we were given.
    shell_input_parts = shell_input.split(' ')
    # Will contain lists of words for each separate command (i.e. separating the
    # shell input parts by pipes).
    command_part_lists = []
    # Will contain words of the command we're currently tracking.
    current_command_parts = []
    # Will contain each finished command, ready for executing.
    commands = []

    # The goal here at first is just to work out where the pipes are.

    # If the whole command was blank, do nothing.
    if not shell_input_parts[0]:
        return

    for part in shell_input_parts:
        # The word might be blank because of whitespace in the original command.
        if not part:
            continue

        if part == '|':
            command_part_lists.append(current_command_parts)
            current_command_parts = []
        else:
            # Variable interpolation
            if part[0] == '$':
                part = data.get_variable(part[1:])

            current_command_parts.append(part)

    command_part_lists.append(current_command_parts)

    for command_parts in command_part_lists:
        current_command_parts = []
        seeking_input_path = False
        seeking_output_path = False
        input_path = None
        output_path = None

        # Now the goal is to work out redirection. Basically, if it encounters < or >
        # it will expect to next see a corresponding file path, and it will hopefully handle
        # cases of malformed input.

        for part in command_parts:
            if (part == '<' or part == '>') and len(current_command_parts) == 0:
                raise Error

            if part == '<':
                seeking_input_path = True
                seeking_output_path = False
            elif part == '>':
                seeking_output_path = True
                seeking_input_path = False
            else:
                if seeking_input_path:
                    if input_path:
                        raise Error

                    input_path = part
                    seeking_input_path = False
                elif seeking_output_path:
                    if output_path:
                        raise Error

                    output_path = part
                    seeking_output_path = False
                else:
                    current_command_parts.append(part)

        command = Command(current_command_parts[0], current_command_parts[1:])
        command.input_path = input_path
        command.output_path = output_path
        commands.append(command)

    for index, command in enumerate(commands):
        # This is where the magic happens!
        command.run()

        # Pipe the stdout to the stdin of the next command if there is one, or connected the stdout
        # to the shell's stdout otherwise.
        if index < len(commands) - 1:
            commands[index + 1].piped_input = command.get_output()
        else:
            return command.get_output()

# This implements the shell loop, which is the same in both interactive
# and file mode.
# It takes two keyword arguments, which return a string command:
# main_input is the input source used for the main input loop,
# and continued_input is used in the case of line continuation.
def shell_loop(**kwargs):
    if 'continued_input' not in kwargs:
        kwargs['continued_input'] = kwargs['main_input']

    while data.loop_is_running:
        try:
            shell_input = kwargs['main_input']()
        except EOFError:
            break

        # Handle line continuation
        while shell_input.endswith('\\'):
            shell_input = shell_input.replace('\\', '')

            try:
                shell_input += kwargs['continued_input']()
            except EOFError:
                break

        output = interpret_input(shell_input)

        if output:
            print(re.sub('\n$', '', output))

def interactive_shell():
    shell_loop(
        main_input=lambda: input(data.get_variable('PS') + ' '),
        continued_input=lambda: input('> ')
    )

def file_interpreter(path):
    file_ = open(path)

    def main_input():
        line = file_.readline()

        if not line:
            raise EOFError

        return line

    shell_loop(main_input=main_input)

    file_.close()

def main(args):
    if len(args):
        file_interpreter(args[0])
    else:
        interactive_shell()

main(sys.argv[1:])
