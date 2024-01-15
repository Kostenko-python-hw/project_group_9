from helper_bot.src.notes.field import Field


class Description(Field):
    def validate(self, value):
        if len(value) <= 80:
            return value
        else:
            raise ValueError("Description must contain at most 80 characters.")

    def check_availability(self, value: str):
        return value in str(self.value).lower()
