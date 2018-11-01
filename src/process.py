import os
import sys
import data

# This is a low level class for forking and executing a child process,
# providing convenience methods for interfacing with its stdin and stdout.

class Process:
    def __init__(self, path, args):
        self.path = path
        self.args = args

        # Data to provide as standard input to the process
        self.input = ''

        inputPipe = os.pipe()
        outputPipe = os.pipe()

        # These names describe whether the ends of the pipe belong to the process
        # (internal) or the parent (external), and whether they provide stdin or
        # stdout for the process.
        self._internalInput = os.fdopen(inputPipe[0], 'r')
        self._externalInput = os.fdopen(inputPipe[1], 'w')
        self._internalOutput = os.fdopen(outputPipe[1], 'w')
        self._externalOutput = os.fdopen(outputPipe[0], 'r')

    # Return's the process' stdout.
    def read(self):
        self._internalOutput.close()
        return self._externalOutput.read()

    def run(self):
        if not os.path.exists(self.path):
            print('Unable to execute ' + self.path)
            return

        pid = os.fork()

        if pid:
            self._internalInput.close()

            # Provide the stdin to the process
            if self.input:
                self._externalInput.write(self.input)

            self._externalInput.close()
            os.wait()
        else:
            self._externalOutput.close()
            self._externalInput.close()

            os.dup2(self._internalOutput.fileno(), sys.stdout.fileno())
            os.dup2(self._internalInput.fileno(), sys.stdin.fileno())
            os.execve(self.path, [self.path] + self.args, data.variables)
            
