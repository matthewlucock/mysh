import sys
import re

args = sys.argv[1:]

if len(args):
    for path in args:
        with open(path) as file_:
            print(re.sub('\n$', '', file_.read()))
else:
    print(input())
