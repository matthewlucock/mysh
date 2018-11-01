import os
import data
from process import Process
import raw_builtins

# This is a class that can be used to execute a fully-featured command on the shell.
# It handles redirection of stdin and stdout given self.input_path and/or
# self.output_path.

class Command:
    def __init__(self, path, args):
        self.path = path
        self.args = args
        self.piped_input = None
        self.input_path = None
        self.output_path = None
        self.process = None

    def run(self):
        if self.path in raw_builtins.functions:
            raw_builtins.functions[self.path](self.args)
            return

        process_builtin_path = data.get_process_builtin_path(self.path)
        if os.path.exists(process_builtin_path):
            self.args = [process_builtin_path] + self.args
            self.path = '/bin/python'

        self.process = Process(self.path, self.args)
        self.process.input = self.piped_input

        if self.input_path:
            with open(self.input_path) as input_file:
                self.process.input = input_file.read()

        self.process.run()

        if self.output_path:
            with open(self.output_path, 'w') as output_file:
                output_file.write(self.process.read())

    def get_output(self):
        # Don't give output to the shell if the output was redirected.
        if self.process and not self.output_path:
            return self.process.read()

        return ''
