import re
import sys

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from helper_bot.src.constants import SHUTDOWN_COMMANDS
from helper_bot.src.contacts.work import add, create, change, show, edit_email, edit_address, edit_birthday, \
    remove_address, remove_birthday, remove_email, remove_phone, find_contact, remove_contact
from helper_bot.src.contacts.work import start, close, search, birthdays
from helper_bot.src.notes.notes_handler import add_note_handler, show_all_notes, search_note, delete_note, edit_note
from helper_bot.src.sorter.sort_folder import sorter_interaction


def help_func():
    reg_exp = re.compile(r'- \*\*.*')

    print('\nList of available commands:\n')
    with open('README.md', 'r') as file:
        while True:
            line = file.readline()
            if not line:
                break

            if re.match(reg_exp, line):
                print(line.replace('*', ''))


general_commands_list = {
    'add note': add_note_handler,
    'show all notes': show_all_notes,
    'search note': search_note,
    'delete note': delete_note,
    'edit note': edit_note,
    'sort folder': sorter_interaction,
    'help': help_func
}

address_book_commands_list = {
    'add phone': add,
    'create contact': create,
    'edit phone': change,
    'show contacts': show,
    'edit email': edit_email,
    'edit address': edit_address,
    'edit birthday': edit_birthday,
    'remove phone': remove_phone,
    'remove email': remove_email,
    'remove birthday': remove_birthday,
    'remove address': remove_address,
    'search contact by name': find_contact,
    'remove contact': remove_contact,
    'search contact': search,
    'birthdays': birthdays
}


def cmd_parser(command, contact_book):
    if command in general_commands_list:
        general_commands_list[command]()
    elif command in address_book_commands_list:
        address_book_commands_list[command](contact_book)
    else:
        print('Command not found')


def main():
    contact_book = start()
    commands = list(address_book_commands_list.keys()) + list(general_commands_list.keys()) + list(SHUTDOWN_COMMANDS)
    commands_completer = WordCompleter(commands)

    while True:
        if sys.stdin.isatty():
            input_date = prompt('Enter the command: ',
                                completer=commands_completer,
                                mouse_support=True,
                                swap_light_and_dark_colors=True,
                                search_ignore_case=True,
                                enable_open_in_editor=True,
                                ).strip().lower()
        else:
            input_date = input('Enter the command: ').strip().lower()

        if input_date in SHUTDOWN_COMMANDS:
            print("Good bye!")
            close(contact_book)
            break
        elif not input_date:
            print('Blank line is not a command.')
        else:
            cmd_parser(input_date, contact_book)


if __name__ == '__main__':
    main()
