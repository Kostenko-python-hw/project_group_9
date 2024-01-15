from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from helper_bot.src.notes.notes_handler import add_note_handler, show_all_notes, search_note, delete_note, edit_note
from helper_bot.src.contacts.work import add, create, change, show, edit_email, edit_address, edit_birthday, remove_address, remove_birthday, remove_email, remove_phone, find_contact, remove_contact
from helper_bot.src.contacts.work import start, close,  search

# @todo move this to config
shutdown_commands = ('good bye', 'close', 'exit')

# @todo make decorator, use it near function definitions, collect all commands to dict and export dict to use in main
command_list = {
    'add note': add_note_handler,
    'show all notes': show_all_notes,
    'search note': search_note,
    'delete note': delete_note,
    'edit note': edit_note,
}

command_list2 = {
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
    'find contact': find_contact,
    'remove contact': remove_contact,
    'search inf': search

}


def cmd_parser(command, contact_book):
    if command in command_list:
        command_list[command]()
    elif command in command_list2:
        command_list2[command](contact_book)
    else:
        print('Command not found')


def main():
    contact_book = start()
    commands_completer = WordCompleter(command_list2)

    while True:
        input_date = prompt('Enter the command: ',
                            completer=commands_completer).strip().lower()

        if input_date in shutdown_commands:
            print("Good bye!")
            close(contact_book)
            break
        elif not input_date:
            print('Blank line is not a command.')
        else:
            cmd_parser(input_date, contact_book)


if __name__ == '__main__':
    main()
