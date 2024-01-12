from src.notes.field import Field


class Title(Field):
    def validate(self, value):
        return value

    def check_availability(self, value: str):
        return value in str(self.value).lower()

    def __str__(self):
        return str(self.value)