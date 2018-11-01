import sys

if len(sys.argv) > 1:
    print(' '.join(sys.argv[1:]))
else:
    try:
        print(input())
    except EOFError:
        print()
