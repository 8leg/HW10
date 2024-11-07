import pathlib

# useful thing
def valid_file(file: str)->bool:
    path = pathlib.Path(file)
    return path.is_file()

# simple input getter to not include it in main function
def get_input()->tuple:
    print('q to exit')
    while True:
        print("Enter name of existing file")
        file=input('> ')
        print("[B]inary or [T]ext?")
        mode=input('> ')
        if 'q' in mode.lower() or 'q'==file:
            exit(0)
        elif mode.lower() in ['b', 't'] and valid_file(file):
            return (file,mode)

# the counter himself
def count_lines(filename: str, mode: str)->int:
    with open(filename, 'r'+mode) as file:
        return len(file.readlines())

# there is no point in using classes for this one so I wont
if __name__ == '__main__':
    while True:
        inp=get_input()
        print(f'there is {count_lines(inp[0], inp[1])} lines in a file')