import sys

def read_input_from_file_or_console(file=None, console_input=None, plain_text=False):
    # Determine the mode for opening the file and reading from stdin
    mode = 'r' if plain_text else 'rb'
    console_read_mode = sys.stdin.read if plain_text else sys.stdin.buffer.read
    
    # Read from file if provided
    if file:
        with open(file, mode) as f:
            content = f.read()
    # Otherwise, read from console input or stdin
    else:
        if console_input is not None:
            content = console_input
        else:
            content = console_read_mode()
    
    return content


def get_bytes(file=None, console_input=None):
    return len(read_input_from_file_or_console(file, console_input))

def get_words(file=None, console_input=None):
    return len(read_input_from_file_or_console(file, console_input).split())

def get_lines(file=None, console_input=None):
    return read_input_from_file_or_console(file, console_input).count(b'\n')

def get_chars(file=None, console_input=None):
    return len(read_input_from_file_or_console(file, console_input, True))





def execute():

    flag = '-d'
    file = None

    if len(sys.argv)==2:
        
        flag = sys.argv[1]
        if flag.startswith('-'):
            file = None
        else:
            file = flag
            flag = '-d' 
    elif len(sys.argv)==3:
        flag = sys.argv[1]
        file = sys.argv[2]

    if flag not in ['-c', '-m', '-l', '-w', '-d']:
        print(f"Invalid option {flag}")
        return

    if flag == '-c':
        print(f"{get_bytes(file)}")
    elif flag == '-l':
        print(f"{get_lines(file)}")
    elif flag == '-w':
        print(f"{get_words(file)}")
    elif flag == '-m':
        print(f"{get_chars(file)}")
    else:
        content = None
        if not file:
            content = sys.stdin.buffer.read() 
        print(get_lines(file,content), get_words(file,content), get_bytes(file,content))



if __name__ == "__main__":
    execute()