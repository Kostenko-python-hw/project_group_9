from helper_bot.src.notes.field import Field


class Tag(Field):
    def validate(self, value):
        return value

    def check_availability(self, value: str):
        return value in self.value
