from src.notes.field import Field


class Title(Field):
    def validate(self, value):
        if len(value) <= 50:
            return value
        else:
            raise ValueError("Title must contain at most 50 characters.")

    def check_availability(self, value: str):
        return value in str(self.value).lower()
    #
    # def __str__(self):
    #     return str(self.value)
