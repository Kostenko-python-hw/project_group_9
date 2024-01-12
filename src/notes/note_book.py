import pickle
from collections import UserDict
from src.notes.note import Note
from src.constants import NOTES_FILE_NAME


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

    def search(self, value: str, option):
        result = set()
        for el in self.data.values():
            record = False
            if option == 'tag':
                record = el.find_by_tag(value)
            elif option == 'content':
                record = el.find_in_content(value)

            if record:
                result.add(str(record))
            if len(result) > 0:
                return '\n'.join([str(record) for record in result])

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

    def edit(self, id, value, option):
        if option == 'title':
            self.data[id].title = value
        elif option == 'description':
            self.data[id].description = value
        elif option == 'tags':
            self.data[id].tags = value.split(',')

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
            pickle.dump({"data": self.data, "notes_counter": self.notes_counter}, fh)
