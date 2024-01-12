from collections import UserDict
from datetime import datetime
import pickle
import re

class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if not self.is_valid(new_value):
            raise ValueError("Incorrect value")
        self.__value = new_value

    def is_valid(self, value):
        return True

    def __str__(self):  
        return str(self.value)


class Name(Field):
    def is_valid(self, value):
        if value.isalpha() :
            return True  
        else:
            return False



class Phone(Field):

    def is_valid(self, new_value):
        return bool(re.match(r'^\d{10}$', new_value))

    def __str__(self):
        return self.value



class Birthday(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value: str):
        if self.is_valid(new_value):
            self.__value = datetime.strptime(new_value, "%d-%m-%Y").date()
        else:
            raise ValueError("Invalid date format. Use DD-MM-YYYY.")

    def is_valid(self, date_str):
        if date_str:
            try:
                datetime.strptime(date_str, "%d-%m-%Y")
                return True
            except ValueError:
                return False


    # def days_to_birthday(self):
    #     if self.__value:
    #         today = datetime.now().date()
    #         next_birthday = datetime(today.year, self.__value.month, self.__value.day).date()
    #         if today > next_birthday:
    #             next_birthday = datetime(today.year + 1, self.__value.month, self.__value.day).date()
    #         days_left = (next_birthday - today).days
    #         return days_left
    #     return None






class Email(Field):
    def is_valid(self, new_value):
        email_pattern = r"[A-Za-z]+[A-Za-z0-9._]+[@]\w{2,}[.]\w{2,3}"
        return bool(re.match(email_pattern, new_value))

    def __str__(self):
        return self.value

class Address(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value

    def __str__(self):
        return self.value

class Record:
    def __init__(self, name, birthday=None, email=None, address=None):
        self.name = Name(name)
        self.phones = []
        if birthday:
            self.birthday = Birthday(birthday)
        else:
            self.birthday = birthday
        if email:
            self.email = Email(email)
        else:
            self.email = email
        if address:
            self.address = Address(address)
        else:
            self.address = address

    def add_phone(self, phone):
        try:
            phone_obj = Phone(phone)
            self.phones.append(phone_obj)
            return f"Phone number {phone} added successfully"
        except ValueError as e:
            return f"Error: {e}"

    def remove_phone(self, phone):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                self.phones.remove(phone_obj)
                return f"Phone number {phone} removed successfully"
        return f"Phone number {phone} not found"

    def edit_phone(self, old_phone, new_phone):
        for phone_obj in self.phones:
            if phone_obj.value == old_phone:
                phone_obj.value = new_phone
                return f"Phone number {old_phone} edited successfully"
        raise ValueError(f"Phone number {old_phone} not found")

    def find_phone(self, phone):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj
        return None
    
    def get_phones(self):
        return [str(phone.value) for phone in self.phones]
    
    def days_to_birthday(self):
        '''
        This method counts days till next birthday of Record object
        '''
        result = None
        if self.birthday:
            today = datetime.now()
            this_year = today.year
            days_b4_birthday = 0

            birthday_date_obj = datetime.strptime(self.birthday.value, '%d-%m-%Y')

            this_year_birthday_obj = datetime(
                year = this_year,
                month = birthday_date_obj.month,
                day = birthday_date_obj.day
                )
            next_year_birthday_obj = datetime(
                year = this_year + 1,
                month = birthday_date_obj.month,
                day = birthday_date_obj.day
                )

            if this_year_birthday_obj < today:
                days_b4_birthday = next_year_birthday_obj - today
            else:
                days_b4_birthday = this_year_birthday_obj - today

            result = days_b4_birthday.days

        else:
            print('The birthday was not stated')

        return result

    def __str__(self):
        phones_str = "; ".join(self.get_phones())
        return f"Contact name: {self.name}, phones: {phones_str}, birthday: {self.birthday}, email: {self.email}, address: {self.address}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    # def iterator(self, batch_size=1):
    #     current_index = 0
    #     while current_index < len(self.data):
    #         yield list(self.data.values())[current_index:current_index + batch_size]
    #         current_index += batch_size

    def find(self, name):
        return self.data.get(name)
    
    
    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return f"Record {name} deleted successfully"
        return f"Record {name} not found"


    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.data = pickle.load(file)
        except (FileNotFoundError, EOFError):
            # Якщо файл не існує або порожній, залишаємо адресну книгу пустою
            self.data = {}

    def search_contacts(self, query):
        results = []
        for record in self.data.values():
            if query.lower() in record.name.value.lower():
                results.append(record)
            for phone_obj in record.phones:
                if query in phone_obj.value:
                    results.append(record)
                    break  # Додавання запису лише один раз
        return results
    
    def contacts_birthdays(self, days):
        '''
        This method returns the contacts whose birthdays will come in next number of "days"
        '''
        result_contacts = []
        for record in self.data.values():
            if record.birthday and record.days_to_birthday() < days:
                result_contacts.append(str(record))

        return result_contacts
        
        

# #Тести
# # Створення нової адресної книги
new_book = AddressBook()

john = Record("John", "20-05-2000", "contact_email123@gmail.com", "Street 45")
john.add_phone("1234567890")
new_book.add_record(john)
print(john) 
print(new_book.find("John"))
# # Завантаження адресної книги з диску
# new_book.load_from_file('address_book.pkl')

# # Створення запису для John
# john_record = Record("John")
# john_record.add_phone("1234567890")
# john_record.add_phone("5555555555")

# # Додавання запису John до адресної книги
# new_book.add_record(john_record)

# # Створення та додавання нового запису для Jane
# jane_record = Record("Jane")
# jane_record.add_phone("9876543210")
# new_book.add_record(jane_record)

# # Виведення всіх записів у книзі
# for name, record in new_book.data.items():
#     print(record)

# # Знаходження та редагування телефону для John
# john = new_book.find("John")
# john.edit_phone("1234567890", "1112223333")

# print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# # Пошук конкретного телефону у записі John
# found_phone = john.find_phone("5555555555")
# print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# # Видалення запису Jane
# new_book.delete("Jane")

# john = Record("John", "20-05-2000", "contact_email123@gmail.com", "Street 45")
# print(john)  # Виведення кількості днів до наступного дня народження

# # Перевірка пагінації
# for batch in new_book.iterator(batch_size=1):
#     for record in batch:
#         print(record)

# new_book.save_to_file('address_book.pkl')