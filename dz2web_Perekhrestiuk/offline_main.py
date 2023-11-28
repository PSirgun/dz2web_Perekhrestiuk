from group2.all_commands import COMMANDS
from group2.terminal_tips import my_input
from group2.service_addressbook import book
from group2.service_notebook import note_book



def parser(text: str):
    for func in COMMANDS.keys():
        if text.startswith(func):
            return func, text[len(func) :].strip().split()

def main():
    while True:
        user_input = my_input()
        func, data = parser(user_input.lower())
        current_func = COMMANDS.get(func)
        print(current_func(*data))


if __name__ == "__main__":
    main()


