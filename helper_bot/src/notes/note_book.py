import pickle
from collections import UserDict

from helper_bot.src.notes.note import Note
from helper_bot.src.storage import NOTES_FILE_NAME


class NoteBook(UserDict):
    def __init__(self):
        # super().__init__()
        try:
            file = self.restore_from_file()
            self.data = file.get("data", {})
            self.notes_counter = file.get("notes_counter", 0)
        except FileNotFoundError:
            self.data = {}
            self.notes_counter = 0

    @property
    def notes_counter(self):
        return self.__notes_counter

    @notes_counter.setter
    def notes_counter(self, value):
        self.__notes_counter = value

    def add(self, data: Note):
        self.data[self.notes_counter] = data
        self.notes_counter += 1
        self.save_to_file()

    def search(self, data: str, option):
        result = {}
        for key, value in self.data.items():
            record = False
            if option == 'tag':
                record = value.find_by_tag(data)
            elif option == 'content':
                record = value.find_in_content(data)

            if record:
                result[key] = record

        if len(result) > 0:
            return result

    def delete(self, id):
        if id in self.data:
            del self.data[id]
            self.save_to_file()
            return True

    def get_note_by_id(self, id):
        if id in self.data:
            return self.data[id]
        else:
            return False

    def edit(self, _id, value, option):
        if option == 'title':
            self.data[_id].title = value
        elif option == 'description':
            self.data[_id].description = value
        elif option == 'tags':
            self.data[_id].tags = value.split(',')

        self.save_to_file()

    def restore_from_file(self):
        try:
            with open(NOTES_FILE_NAME, "rb") as fh:
                file = pickle.load(fh)
            return file
        except FileNotFoundError:
            return {}

    def save_to_file(self):
        with open(NOTES_FILE_NAME, "wb") as fh:
            pickle.dump(
                {"data": self.data, "notes_counter": self.notes_counter}, fh)
