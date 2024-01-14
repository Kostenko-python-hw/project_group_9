
from src.notes.notes_handler import add_note_handler, show_all_notes, search_note, delete_note, edit_note
from src.contacts.work import add, create, change, show, edit_email, edit_address, edit_birthday, remove_address, remove_birthday, remove_email, remove_phone, find_contact, remove_contact
from src.contacts.work import start, close


shutdown_commands = ('good bye', 'close', 'exit')

command_list = {
    'add_note': add_note_handler,
    'show_all_notes': show_all_notes,
    'search_note': search_note,
    'delete_note': delete_note,
    'edit_note': edit_note,
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
    'remove contact': remove_contact

}

def cmd_parser(command, contact_book):
    if command in command_list:
        command_list[command]()
    elif command in command_list2:
        command_list2[command](contact_book)
    else:
        print('Command not found')


def global_handler():
    contact_book = start()
    while True:
        input_date = input('Enter the command:').strip().lower()

        if input_date in shutdown_commands:
            print("Good bye!")
            close(contact_book)
            break
        elif not input_date:
            print('Blank line is not a command.')
        else:
            cmd_parser(input_date, contact_book)


def main():
    global_handler()


if __name__ == '__main__':
    main()