from src.constants import CONTACTS_FILE_NAME
from src.contacts.classes import Record, AddressBook, Phone, Email
from pathlib import Path
from src.constants import bcolors


def create(contact_book: AddressBook):
    while True:
        name = input('Enter name: ')
        if name.isalpha():
            break
        else:
            print(f"{bcolors.FAIL}Incorrect value{bcolors.ENDC}")
    while True:
        phone = input('Enter phone  ')
        try:
            Phone(phone)
            break
        except:
            print('Incorrect value')
            continue
    
    while True:
        email = input('Enter email  ')
        if email == '':
            email = None
            break
        try:
            Email(email)
            break
        except:
            print('Incorrect value')
            continue
    address = input('Enter address  ')
    if address == '':
        address = None
    birthday = input('Enter birthday  ')
    if birthday == '':
        birthday = None
    new_contact = Record(name, birthday, email, address)
    new_contact.add_phone(phone)
    contact_book.add_record(new_contact)


def add(contact_book: AddressBook):
    while True:
        name = input('Enter name   ')
        if name.isalpha():
            break
        else:
            print('Incorrect value')
    for el in contact_book.data.values():
        if name == el.name.value:
            while True:
                phone = input('Enter phone  ')
                try:
                    Phone(phone)
                    break
                except:
                    print('Incorrect value')
                    continue 
            el.add_phone(phone)
            return 'added'
    print('There is not such name in the contact book ' )  


def change(contact_book: AddressBook):
    while True:
        phone = input('Enter phone  ')
        try:
            Phone(phone)
            break
        except:
            print('Incorrect value')
            continue
    for phone_contact_book in contact_book.data.values():
        for tel in phone_contact_book.phones:
            if phone == tel.value:
                while True:
                    new_phone = input('Enter new phone  ')
                    try:
                        Phone(new_phone)
                        break
                    except:
                        print('Incorrect value')
                        continue
                phone_contact_book.edit_phone(phone, new_phone)
                return 'changed'
    print('There is not such number in the contact book '  )     


def show(contact_book: AddressBook):
    print(contact_book.list_contacts())


def start():
    if Path(CONTACTS_FILE_NAME).is_file():
        return AddressBook.load_from_file(CONTACTS_FILE_NAME)
    else:
        return AddressBook()


def close(contact_book: AddressBook):
    contact_book.save_to_file(CONTACTS_FILE_NAME)
    

def edit_email(contact_book: AddressBook):
    while True:
        name = input('Enter name   ')
        if name.isalpha():
            break
        else:
            print('Incorrect value')
    for el in contact_book.data.values():
        if name == el.name.value:
            while True:
                email = input('Enter email  ')
                try:
                    Email(email)
                    break
                except:
                    print('Incorrect value')
                    continue
            el.edit_email(email)
            return  "Email edited successfully"   
    print('There is no contact with such name in the contact book' )   


def edit_birthday(contact_book: AddressBook):
    while True:
        name = input('Enter name   ')
        if name.isalpha():
            break
        else:
            print('Incorrect value')
    
    for el in contact_book.data.values():
        if name == el.name.value:
            birthday = input('Enter birthday  ')
            el.edit_birthday(birthday)
            return 'done'
    print( 'There is no contact with such name in the contact book' )


def edit_address(contact_book: AddressBook):
    while True:
        name = input('Enter name   ')
        if name.isalpha():
            break
        else:
            print('Incorrect value') 
    for el in contact_book.data.values():
        if name == el.name.value:
            address = input('Enter address  ')
            el.edit_address(address)
            return  "Email edited successfully"   
    print('There is no contact with such name in the contact book' )


def remove_phone(contact_book: AddressBook):
    while True:
        name = input('Enter name   ')
        if name.isalpha():
            break
        else:
            print('Incorrect value')
    for el in contact_book.data.values():
        if name == el.name.value:
            while True:
                phone = input('Enter phone  ')
                try:
                    Phone(phone)
                    break
                except:
                    print('Incorrect value')
                    continue
            return el.remove_phone(phone)          
    print( 'There is no contact with such name in the contact book' )
 

def remove_email(contact_book: AddressBook):
    while True:
        name = input('Enter name   ')
        if name.isalpha():
            break
        else:
            print('Incorrect value')
    for el in contact_book.data.values():
        if name == el.name.value:
            return el.remove_email()          
    return 'There is no contact with such name in the contact book' 


def remove_address(contact_book: AddressBook):
    while True:
        name = input('Enter name   ')
        if name.isalpha():
            break
        else:
            print('Incorrect value')
    for el in contact_book.data.values():
        if name == el.name.value:
            el.remove_address()
            return 'removed'         
    return 'There is no contact with such name in the contact book' 


def remove_birthday(contact_book: AddressBook):
    while True:
        name = input('Enter name   ')
        if name.isalpha():
            break
        else:
            print('Incorrect value')
    for el in contact_book.data.values():
        if name == el.name.value:
            return el.remove_birthday()        
    return 'There is no contact with such name in the contact book' 


def find_contact(contact_book: AddressBook):
    while True:
        name = input('Enter name   ')
        if name.isalpha():
            break
        else:
            print('Incorrect value')
    contact_book.find(name)   


def remove_contact(contact_book: AddressBook):
    while True:
        name = input('Enter name   ')
        if name.isalpha():
            break
        else:
            print('Incorrect value')
    contact_book.delete(name) 
       

