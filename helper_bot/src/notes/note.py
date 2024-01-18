from helper_bot.src.notes.description import Description
from helper_bot.src.notes.tag import Tag
from helper_bot.src.notes.title import Title


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
