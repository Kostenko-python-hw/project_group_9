from note_classes import Tag, Title, Description, Note, Notes
from constants import bcolors

shutdown_commands = ('good bye', 'close', 'exit')


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


def add_note_handler():
    new_note = Note()
    # add title
    title = input('Enter a title:').strip()
    new_note.title = Title(title)
    # add description
    description = input('Enter a description:').strip()
    new_note.description = Description(description)
    if title == '' and description == '':
        print(f"{bcolors.FAIL}Note can't be without a title and description{bcolors.ENDC}")
    else:
        # add tags
        print(f"{bcolors.WARNING}Multiple tags can be separated with a comma{bcolors.ENDC}")
        tags = input('Enter tags:').strip()
        splitted_tags = tags.split(',')
        list_of_tags = list(map(lambda el: Tag(el.strip().lower()), splitted_tags))
        new_note.add_tag(list_of_tags)
        #add new note to notes list
        notes_database = Notes()
        try:
            notes_database.add(new_note)
            print(f"{bcolors.OKGREEN}The note has been successfully added{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL}Something went wrong{bcolors.ENDC}")



def show_all_notes():
    notes_database = Notes()
    if len(notes_database) == 0:
        return 'You don\'t have any notes yet.'
    else:
        for key, note in notes_database.items():
            print(f'{key} {note}') # добавить красивый вывод


def search_note():
    print("Choose an option:")
    print("1. Search in tags")
    print("2. Search in content")
    print("3. Exit")

    choice = input("Enter the number of your choice: ")

    if choice == "1":
        search = input("Search: ")
        notes_database = Notes()
        result = notes_database.search(search.lower().strip(), 'tag')
        print(f'Result: {result}')
    elif choice == "2":
        search = input("Search: ")
        notes_database = Notes()
        result = notes_database.search(search.lower().strip(), 'content')
        print('Result')
        print(result)
    elif choice == '3':
        return #добавить выход потом
    else:
        print("Invalid choice. Please enter a valid number.")


def delete_note():
    print(f"{bcolors.WARNING}If you don't know the id, you can use search_note to search for the note, or show_all_notes to display all notes{bcolors.ENDC}")
    print(f"{bcolors.OKBLUE}Enter q to exit{bcolors.ENDC}")
# добавить перевод валуе в int и обработчик ошибок
    id = input("Enter the id of the note you want to delete: ")

    if id == "q":
        return
    elif not id:
        print('Blank line is not a id.')
    else:
        try:
            notes_database = Notes()
            isDeleted = notes_database.delete(int(id))
            if isDeleted:
                print('The note was successfully deleted')
            else:
                print('Id not found')
        except ValueError:
            print('The id must be a number')
   

def edit_note():
    print(f"{bcolors.WARNING}If you don't know the id, you can use search_note to search for the note, or show_all_notes to display all notes{bcolors.ENDC}")
    print(f"{bcolors.OKBLUE}Enter q to exit{bcolors.ENDC}")
# добавить перевод валуе в int и обработчик ошибок
    id = input("Enter the id of the note you want to edit: ")

    if id == "q":
        return
    elif not id:
        print('Blank line is not a id.')
    else:
        notes_database = Notes()
        current_note = False
        try:
            current_note = notes_database.get_note_by_id(int(id))
        except ValueError:
            print('The id must be a number')

        if not current_note:
            print('Id not found')
        else:
            print("Choose an option:")
            print("1. Edit title")
            print("2. Edit description")
            print("3. Edit tags")
            print("4. Exit")

            choice = input("Enter the number of your choice: ")

            if choice == "1":
                new_title = input("Enter a new title: ")
                notes_database.edit(int(id), new_title, 'title')
                print('The title was successfully edited')
            elif choice == "2":
                new_description = input("Enter a new description: ")
                notes_database.edit(int(id), new_description, 'description')
                print('The description was successfully edited')
            elif choice == "3":
                print(f"{bcolors.WARNING}Multiple tags can be separated with a comma{bcolors.ENDC}")
                new_tags = input("Enter new tags: ")
                notes_database.edit(int(id), new_tags, 'tags')
                print('The tags was successfully edited')
            elif choice == '4':
                return #добавить выход потом
            else:
                print("Invalid choice. Please enter a valid number.")
     

command_list = {
    'add_note': add_note_handler,
    'show_all_notes': show_all_notes,
    'search_note': search_note,
    'delete_note': delete_note,
    'edit_note': edit_note,
}

def main():
    global_handler()


if __name__ == '__main__':
    main()