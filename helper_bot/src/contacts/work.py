import datetime
from pathlib import Path

from helper_bot.src.constants import bcolors
from helper_bot.src.contacts.classes import Record, AddressBook, Phone, Email, Birthday, Name
from helper_bot.src.storage import CONTACTS_FILE_NAME


def close(contact_book: AddressBook):
    contact_book.save_to_file(CONTACTS_FILE_NAME)


def valid_name():
    while True:
        name = input('Enter contact name: ')
        try:
            Name(name)
            return name
        except:
            print(f"{bcolors.FAIL}Incorrect value{bcolors.ENDC}")


def valid_phone():
    while True:
        print(
            f'Example phone number: {bcolors.OKGREEN}0673804545{bcolors.ENDC}')
        phone = input('Enter phone number:   ')
        try:
            Phone(phone)
            return phone
        except:
            print(f"{bcolors.FAIL}Incorrect value{bcolors.ENDC}")


def valid_email():
    while True:
        print(f'Example email: {bcolors.OKGREEN}goit@gmail.com{bcolors.ENDC}')
        email = input('Enter email:   ')
        if email == '':
            email = None
            return None
        try:
            Email(email)
            return email
        except:
            print(f"{bcolors.FAIL}Incorrect value{bcolors.ENDC}")


def valid_birthday():
    while True:
        print(f'Example birthday: {bcolors.OKGREEN}12-01-1991{bcolors.ENDC}')
        birthday = input('Enter birthday:   ')
        if birthday == '':
            birthday = None
            return None
        try:
            birth = Birthday(birthday)
            today = datetime.date.today()
            current_year = today.year
            if 1900 < birth.value.year < current_year:
                return birthday
            else:
                print('Year must be appropriate to the age')
        except:
            print(f"{bcolors.FAIL}Incorrect value{bcolors.ENDC}")


def create(contact_book: AddressBook):
    while True:
        name = valid_name()
        i = True
        for el in contact_book.keys():
            if name.lower() == el.lower():
                i = False
                print(f' There is a contact with  name {name} in Contact book')
                break
        if i == True:
            break
    phone = valid_phone()
    email = valid_email()
    address = input('Enter address:  ')
    if address == '':
        address = None
    birthday = valid_birthday()
    new_contact = Record(name, birthday, email, address)
    new_contact.add_phone(phone)
    contact_book.add_record(new_contact)
    print(
        f'Contact {bcolors.OKBLUE}{name}{bcolors.ENDC} has been created successfully')
    close(contact_book)


def add(contact_book: AddressBook):
    name = valid_name()
    for el in contact_book.data.values():
        if name.lower() == el.name.value.lower():
            phone = valid_phone()
            el.add_phone(phone)
            print(
                f"Phone has been added to contact {bcolors.OKBLUE}{name}{bcolors.ENDC}")
            close(contact_book)
            return 'added'
    print(
        f'There is not contact witn name {bcolors.FAIL}{name}{bcolors.ENDC} in the contact book ')


def change(contact_book: AddressBook):
    name = valid_name()
    for el in contact_book.data.values():
        if name.lower() == el.name.value.lower():
            print(f"{bcolors.OKBLUE}{str(el)}{bcolors.ENDC}")
            while True:
                phone = input('Enter contact phone number:   ')
                try:
                    Phone(phone)
                    break
                except:
                    print(f"{bcolors.FAIL}Incorrect value{bcolors.ENDC}")
            for tel in el.phones:
                if phone == tel.value:
                    while True:
                        new_phone = input('Enter new phone number:  ')
                        try:
                            Phone(new_phone)
                            break
                        except:
                            print(f"{bcolors.FAIL}Incorrect value{bcolors.ENDC}")
                            continue
                    el.edit_phone(phone, new_phone)
                    print(
                        f"Phone number {bcolors.OKBLUE}{phone}{bcolors.ENDC} has been replaced by {bcolors.OKGREEN}{new_phone}{bcolors.ENDC}")
                    close(contact_book)
                    return 'changed'
            print(f'Contact {name} has not phone {phone}')
            return None
    print(
        f'There is not contact witn name {bcolors.FAIL}{name}{bcolors.ENDC} in the contact book ')


def show(contact_book: AddressBook):
    res = contact_book.list_contacts()
    res2 = (' ;\n').join(res)
    if res == []:
        print('There are no contacts in Contact book')
        return None
    print(res2)


def start():
    if Path(CONTACTS_FILE_NAME).is_file():
        return AddressBook.load_from_file(CONTACTS_FILE_NAME)
    else:
        return AddressBook()


def edit_email(contact_book: AddressBook):
    name = valid_name()
    for el in contact_book.data.values():
        if name.lower() == el.name.value.lower():
            email = valid_email()
            el.edit_email(email)
            close(contact_book)
            return "Email edited successfully"
    print(
        f'There is not contact witn name {bcolors.FAIL}{name}{bcolors.ENDC} in the contact book ')


def edit_birthday(contact_book: AddressBook):
    name = valid_name()
    for el in contact_book.data.values():
        if name.lower() == el.name.value.lower():
            birthday = valid_birthday()
            el.edit_birthday(birthday)
            close(contact_book)
            return 'done'
    print(
        f'There is not contact witn name {bcolors.FAIL}{name}{bcolors.ENDC} in the contact book ')


def edit_address(contact_book: AddressBook):
    name = valid_name()
    for el in contact_book.data.values():
        if name.lower() == el.name.value.lower():
            address = input('Enter address  ')
            el.edit_address(address)
            close(contact_book)
            return "Email edited successfully"
    print(
        f'There is not contact witn name {bcolors.FAIL}{name}{bcolors.ENDC} in the contact book ')


def remove_phone(contact_book: AddressBook):
    name = valid_name()
    for el in contact_book.data.values():
        if name.lower() == el.name.value.lower():
            if len(el.phones) == 1:
                print(
                    f'Sorry, you can"t remove phone number.Contact {bcolors.FAIL}{el.name.value}{bcolors.ENDC} has only one phone.')
                return None
            else:
                phone = valid_phone()
                print(
                    f"Phone number {bcolors.FAIL}{phone}{bcolors.ENDC} removed successfully")
                el.remove_phone(phone)
                close(contact_book)
                return 'done'
    print(
        f'There is not contact witn name {bcolors.FAIL}{name}{bcolors.ENDC} in the contact book ')


def remove_email(contact_book: AddressBook):
    name = valid_name()
    for el in contact_book.data.values():
        if name.lower() == el.name.value.lower():
            el.remove_email()
            close(contact_book)
            return 'done'
    print(
        f'There is not contact witn name {bcolors.FAIL}{name}{bcolors.ENDC} in the contact book ')


def remove_address(contact_book: AddressBook):
    name = valid_name()
    for el in contact_book.data.values():
        if name.lower() == el.name.value.lower():
            el.remove_address()
            close(contact_book)
            return 'removed'
    print(
        f'There is not contact witn name {bcolors.FAIL}{name}{bcolors.ENDC} in the contact book ')


def remove_birthday(contact_book: AddressBook):
    name = valid_name()
    for el in contact_book.data.values():
        if name.lower() == el.name.value.lower():
            el.remove_birthday()
            close(contact_book)
            return 'done'
    print(
        f'There is not contact witn name {bcolors.FAIL}{name}{bcolors.ENDC} in the contact book ')


def find_contact(contact_book: AddressBook):
    name = valid_name()
    contact_book.find(name)


def remove_contact(contact_book: AddressBook):
    name = valid_name()
    contact_book.delete(name)
    close(contact_book)


def birthdays(contact_book: AddressBook):
    while True:
        quant = input('Enter quantity of days:   ')
        if quant.isdigit() and 0 < int(quant) < 365:
            break
        else:
            print('Incorrect value')
    quant = int(quant)
    contact_book.contacts_birthdays(quant)


def search(contact_book: AddressBook):
    inf = input('Enter information about contact:   ')
    res = contact_book.find_inf(inf)
    res2 = (' ;\n').join(res)
    if res == []:
        print('There isn"t any contact with such information')
    print(res2)
