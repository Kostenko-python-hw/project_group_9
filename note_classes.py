import pickle
from collections import UserDict
from constants import NOTES_FILE_NAME

############ FIELD ############
class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = self.validate(value)

    def validate(self, _):
        pass

    def check_availability(self, value: str):
        pass

    def __str__(self):
        return str(self.value)
    
############ TITLE ############
class Title(Field):
    def validate(self, value):
        return value

    def check_availability(self, value: str):
        return value in str(self.value).lower()

    def __str__(self):
        return str(self.value)
    
############ DESCRIPTION ############
class Description(Field):
    def validate(self, value):
        return value
    
    def check_availability(self, value: str):
        return value in str(self.value).lower()

    def __str__(self):
        return str(self.value)
    
############ TAG ############
class Tag(Field):
    def validate(self, value):
        return value

    def check_availability(self, value: str):
        return value in self.value
    
############ _NOTE_ ############
class Note:
    def __init__(self):
        self.__title = None
        self.__description = None
        self.__tags = None
        self.title = ''
        self.description = ''
        self.tags = []  

    @property
    def title(self):
        return self.__title
    
    @property
    def description(self):
        return self.__description
    
    @property
    def tags(self):
        return self.__tags
    

    @title.setter
    def title(self, value):
        self.__title = Title(value)

    @description.setter
    def description(self, value):
        self.__description = Description(value)

    @tags.setter
    def tags(self, value):
        self.__tags = list(map(lambda el: Tag(el), value))

    def add_tag(self, tags):
        self.tags.extend(tags)
            
    def find_by_tag(self, value):
        for tag in self.tags:
            is_exist_in_tags = tag.check_availability(value)
            if is_exist_in_tags:
                return self
            
    def find_in_content(self, value):
        is_exist_in_title = self.title.check_availability(value)

        if is_exist_in_title:
            return self
        
        is_exist_in_description = self.description.check_availability(value)

        if is_exist_in_description: 
            return self
        
    def __str__(self):
        return f"Title: {self.title}, description: {self.description}, tags: {', '.join(p.value for p in self.tags)}"


############ NOTES ############
class Notes(UserDict):
    def __init__(self):
        try:
            file = self.restore_from_file()
            self.data = file["data"]
            self.notes_counter = file.get("notes_counter", 0)
        except:
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


    ######## 
    def restore_from_file(self):
        try:
            with open(NOTES_FILE_NAME, "rb") as fh:
                file = pickle.load(fh)
            return file
        except FileNotFoundError:
            return {}
    
    # @classmethod
    def save_to_file(self):
        with open(NOTES_FILE_NAME, "wb") as fh:
            pickle.dump({"data": self.data, "notes_counter": self.notes_counter}, fh)
    ######## 