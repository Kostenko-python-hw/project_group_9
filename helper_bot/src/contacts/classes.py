import pickle
import re
from collections import UserDict
from datetime import datetime

from helper_bot.src.constants import bcolors


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
        value2 = value.split(' ')
        for el in value2:
            if not el.isalpha():
                return False
        return True


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

    def edit_birthday(self, new_birthday):
        self.birthday = Birthday(new_birthday)
        print("Birthday has been edited successfully")

    def edit_email(self, new_email):
        self.email = Email(new_email)
        print("Email has been edited successfully")

    def edit_address(self, new_address):
        self.address = Address(new_address)
        print("Address has been edited successfully")

    def remove_email(self):
        self.email = None
        print("Email has been removed successfully")

    def remove_birthday(self):
        self.birthday = None
        print("Birthday has been removed successfully")

    def remove_address(self):
        self.address = None
        print("Address has been removed successfully")

    def add_phone(self, phone):
        try:
            phone_obj = Phone(phone)
            self.phones.append(phone_obj)
        except ValueError as e:
            return f"Error: {e}"

    def remove_phone(self, phone):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                self.phones.remove(phone_obj)

                return 'done'
        print(f"Phone number {phone} not found")

    def edit_phone(self, old_phone, new_phone):
        for phone_obj in self.phones:
            if phone_obj.value == old_phone:
                phone_obj.value = new_phone

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

            this_year_birthday_obj = datetime(
                year=this_year,
                month=self.birthday.value.month,
                day=self.birthday.value.day
            )
            next_year_birthday_obj = datetime(
                year=this_year + 1,
                month=self.birthday.value.month,
                day=self.birthday.value.day
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
        return f"Contact name: {bcolors.OKBLUE}{self.name}{bcolors.ENDC}, phones:{bcolors.OKGREEN} {phones_str}{bcolors.ENDC}, birthday: {bcolors.WARNING}{self.birthday}{bcolors.ENDC}, email: {bcolors.WARNING}{self.email}{bcolors.ENDC}, address: {bcolors.WARNING}{self.address}{bcolors.ENDC}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def list_contacts(self):
        output = []
        for el in self.data.values():
            output.append(str(el))
        return output

    def find_inf(self, inf: str):
        output = []
        if inf.isalpha():
            for el in self.data.values():
                if inf.lower() in el.name.value.lower():
                    output.append(str(el))
        elif inf.isdigit():
            for el in self.data.values():
                for i in el.phones:
                    if inf in i.value:
                        output.append(str(el))
                        break
        return output

    def find(self, name):
        for el in self.data:
            if name.lower() == el.lower():
                print(str(self.data[el]))
                return 'Done'

        print(f'There isn"t contact with  {bcolors.FAIL}{name}{bcolors.ENDC} name')

    def delete(self, name):
        for el in self.data:
            if name.lower() == el.lower():
                self.data.pop(el)
                print(f"Contact {bcolors.OKBLUE}{name}{bcolors.ENDC} has been deleted successfully")
                return 'done'
        print(f"Contact {bcolors.FAIL}{name}{bcolors.ENDC} not found")

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self, file)

    def load_from_file(filename):
        with open(filename, "rb") as fh:
            unpacked = pickle.load(fh)
        return unpacked

    def search(self, search_str):
        '''
        method searches contacts which name or phones match with "search string"
        '''
        result = []
        for abonent_name, abonent_obj in self.data.items():

            if search_str.lower() in abonent_name.lower():
                result.append(str(abonent_obj))
                continue

            if abonent_obj.address and search_str.lower() in abonent_obj.address.value.lower():
                result.append(str(abonent_obj))
                continue

            if abonent_obj.email and search_str.lower() in abonent_obj.email.value.lower():
                result.append(str(abonent_obj))
                continue

            for phone in abonent_obj.phones:
                if search_str in phone.value:
                    result.append(str(abonent_obj))
                    break

        return result

    def contacts_birthdays(self, days):
        '''
        This method returns the contacts whose birthdays will come in next number of "days"
        '''
        flag = False
        for record in self.data.values():
            if record.birthday and record.days_to_birthday() < days:
                print(record)
                flag = True

        if not flag:
            print('All contacts have no birthdays during this period')
