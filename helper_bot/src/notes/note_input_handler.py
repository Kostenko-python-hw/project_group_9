from helper_bot.src.notes.tag import Tag
from helper_bot.src.constants import bcolors


class NoteInputHandler:
    @staticmethod
    def get_user_input(prompt):
        return input(prompt).strip()

    def get_title(self, new_note):
        print(
            f"{bcolors.WARNING}Title must contain at most 50 characters.{bcolors.ENDC}")

        while True:
            title = self.get_user_input("Enter a title:")
            if title == 'q':
                return None
            try:
                new_note.title = title
                return
            except ValueError as e:
                print(f"{bcolors.FAIL}{e}{bcolors.ENDC}")

    def get_description(self, new_note):
        print(
            f"{bcolors.WARNING}Description must contain at most 80 characters.{bcolors.ENDC}")
        while True:
            description = self.get_user_input("Enter a description:")
            if description == 'q':
                return None
            try:
                new_note.description = description
                return
            except ValueError as e:
                print(f"{bcolors.FAIL}{e}{bcolors.ENDC}")

    def get_tags(self, new_note):
        print(
            f"{bcolors.WARNING}Tags must contain at most 40 characters.{bcolors.ENDC}")
        print(
            f"{bcolors.OKBLUE}Multiple tags can be separated with a comma{bcolors.ENDC}")
        while True:
            tags_input = self.get_user_input("Enter tags:")
            if len(tags_input) <= 80:
                if tags_input == 'q':
                    return None
                split_tags = tags_input.split(',')
                tag_dict = {}
                for tag_name in split_tags:
                    tag_name = tag_name.strip().lower()
                    if tag_name:
                        tag_instance = Tag(tag_name)
                        tag_dict[tag_name] = tag_instance
                new_note.add_tag(tag_dict.values())
                return
            else:
                print(
                    f"{bcolors.FAIL}Tags must contain at most 40 characters.{bcolors.ENDC}")
