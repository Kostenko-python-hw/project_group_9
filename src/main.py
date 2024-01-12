from notes.notes_handler import add_note_handler, show_all_notes, search_note, delete_note, edit_note

shutdown_commands = ('good bye', 'close', 'exit')

command_list = {
    'add_note': add_note_handler,
    'show_all_notes': show_all_notes,
    'search_note': search_note,
    'delete_note': delete_note,
    'edit_note': edit_note,
}


def cmd_parser(command):
    if command in command_list:
        command_list[command]()
    else:
        print('Command not found')


def global_handler():
    while True:
        input_date = input('Enter the command:').strip().lower()

        if input_date in shutdown_commands:
            print("Good bye!")
            break
        elif not input_date:
            print('Blank line is not a command.')
        else:
            cmd_parser(input_date)


def main():
    global_handler()


if __name__ == '__main__':
    main()