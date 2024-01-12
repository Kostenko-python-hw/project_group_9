from note_classes import Tag, Title, Description, Note, Notes
from constants import bcolors

shutdown_commands = ('good bye', 'close', 'exit')


def cmd_parser(command):
    if command in command_list:
        command_list[command]()
    else:
        print('Command not found')


######## MAIN _NOTE ########
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

######## ADD _NOTE_ ########
def add_note_handler():
    new_note = Note()
    print(f"{bcolors.OKBLUE}Enter q to exit{bcolors.ENDC}")

    while True:
        # add title
        title = input('Enter a title:').strip()
        if title == 'q':
            break
        new_note.title = Title(title)
        # add description
        description = input('Enter a description:').strip()
        if description == 'q':
            break
        new_note.description = Description(description)
        if title == '' and description == '':
            print(f"{bcolors.FAIL}Note can't be without a title and description{bcolors.ENDC}")
        else:
            # add tags
            print(f"{bcolors.WARNING}Multiple tags can be separated with a comma{bcolors.ENDC}")
            tags = input('Enter tags:').strip()
            if tags == 'q':
                break
            splitted_tags = tags.split(',')
            # cleaned_tags = list(filter(lambda el: el.strip(), splitted_tags))
            # list_of_tags = list(map(lambda el: Tag(el.strip().lower()), cleaned_tags))
            tag_dict = {}
            for tag_name in splitted_tags:
                tag_name = tag_name.strip().lower()
                if tag_name:
                    tag_instance = Tag(tag_name)
                    tag_dict[tag_name] = tag_instance

            new_note.add_tag(list(tag_dict.values()))
            #add new note to notes list
            notes_database = Notes()
            try:
                notes_database.add(new_note)
                print(f"{bcolors.OKGREEN}The note has been successfully added{bcolors.ENDC}")
            except:
                print(f"{bcolors.FAIL}Something went wrong{bcolors.ENDC}")
            break


######## SHOW ALL NOTES ########
def show_all_notes():
    notes_database = Notes()
    if len(notes_database) == 0:
        print('You don\'t have any notes yet.')
    else:
        for key, note in notes_database.items():
            print(f'{key} {note}') #добавить вывод в виде таблицы

######## SEARCH _NOTE ########
def search_note():
    print("Choose an option:")
    print("1. Search in tags")
    print("2. Search in content")
    print("3. Exit")

    while True:
        choice = input("Enter the number of your choice: ")

        if choice == "1":
            search = input("Search: ")
            notes_database = Notes()
            result = notes_database.search(search.lower().strip(), 'tag')
            if result:
                print(f"{bcolors.OKGREEN}Result{bcolors.ENDC}")
                print(result) #добавить вывод в виде таблицы и также выводить id
                break
            else:
                print('No results found for the query.')
        elif choice == "2":
            search = input("Search: ")
            notes_database = Notes()
            result = notes_database.search(search.lower().strip(), 'content')
            if result:
                print(f"{bcolors.OKGREEN}Result{bcolors.ENDC}")
                print(result) #добавить вывод в виде таблицы и также выводить id
                break
            else:
                print('No results found for the query.')
        elif choice == '3':
            break 
        else:
            print("Invalid choice. Please enter a valid number.")

######## DELETE _NOTE ########
def delete_note():
    print(f"{bcolors.WARNING}If you don't know the id, you can use search_note to search for the note, or show_all_notes to display all notes{bcolors.ENDC}")
    print(f"{bcolors.OKBLUE}Enter q to exit{bcolors.ENDC}")

    while True:
        id = input("Enter the id of the note you want to delete: ")

        if id == "q":
            break
        elif not id:
            print('Blank line is not a id.')
        else:
            try:
                notes_database = Notes()
                isDeleted = notes_database.delete(int(id))
                if isDeleted:
                    print(f"{bcolors.OKGREEN}The note was successfully deleted{bcolors.ENDC}")
                    break
                else:
                    print('Id not found')
            except ValueError:
                print('The id must be a number')
   

######## EDIT _NOTE ########
def edit_note():
    print(f"{bcolors.WARNING}If you don't know the id, you can use search_note to search for the note, or show_all_notes to display all notes{bcolors.ENDC}")
    print(f"{bcolors.OKBLUE}Enter q to exit{bcolors.ENDC}")
    while True:
        id = input("Enter the id of the note you want to edit: ")

        if id == "q":
            break
        elif not id:
            print('Blank line is not a id.')
        else:
            notes_database = Notes()
            current_note = False
            try:
                current_note = notes_database.get_note_by_id(int(id))
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
                        print(f"{bcolors.OKGREEN}The title was successfully edited{bcolors.ENDC}")
                        break
                    elif choice == "2":
                        new_description = input("Enter a new description: ")
                        notes_database.edit(int(id), new_description, 'description')
                        print(f"{bcolors.OKGREEN}The description was successfully edited{bcolors.ENDC}")
                        break
                    elif choice == "3":
                        print(f"{bcolors.WARNING}Multiple tags can be separated with a comma{bcolors.ENDC}")
                        new_tags = input("Enter new tags: ")
                        notes_database.edit(int(id), new_tags, 'tags')
                        print(f"{bcolors.OKGREEN}The tags was successfully edited{bcolors.ENDC}")
                        break
                    elif choice == '4':
                        break 
                    else:
                        print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print('The id must be a number')

           
     
######## SLIST OF COMMANDS ########
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