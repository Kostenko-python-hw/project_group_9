from src.constants import CONTACTS_FILE_NAME
from src.contacts.classes import Record, AddressBook, Phone, Email, Birthday
from pathlib import Path
from src.constants import bcolors


def close(contact_book: AddressBook):
    contact_book.save_to_file(CONTACTS_FILE_NAME)
    

def create(contact_book: AddressBook):
    while True:
        name = input('Enter contact name: ')
        if name.isalpha():
            break
        else:
            print(f"{bcolors.FAIL}Incorrect value{bcolors.ENDC}")
    while True:
        print(f'Example phone number: {bcolors.OKGREEN}1234525680{bcolors.ENDC}')
        phone = input('Enter phone number:   ')
        try:
            Phone(phone)
            break
        except:
            print(f"{bcolors.FAIL}Incorrect value{bcolors.ENDC}")
            continue 
    while True:
        email = input('Enter email:   ')
        if email == '':
            email = None
            break
        try:
            Email(email)
            break
        except:
            print(f"{bcolors.FAIL}Incorrect value{bcolors.ENDC}")
            continue
    address = input('Enter address:  ')
    if address == '':
        address = None
    while True:
        print(f'Example birthday: {bcolors.OKGREEN}12-01-1991{bcolors.ENDC}')
        birthday = input('Enter birthday:   ')
        if birthday == '':
            birthday = None
            break
        try:
            Birthday(birthday)
            break
        except:
            print(f"{bcolors.FAIL}Incorrect value{bcolors.ENDC}")
            continue
    new_contact = Record(name, birthday, email, address)
    new_contact.add_phone(phone)
    contact_book.add_record(new_contact)
    print(f'Contact {bcolors.OKGREEN}{name}{bcolors.ENDC} has been created successfully')
    close(contact_book)


def add(contact_book: AddressBook):
    while True:
        name = input('Enter contact name:   ')
        if name.isalpha():
            break
        else:
            print(f"{bcolors.FAIL}Incorrect value{bcolors.ENDC}")
    for el in contact_book.data.values():
        if name == el.name.value:
            while True:
                print(f'Example phone number: {bcolors.OKGREEN}1234525680{bcolors.ENDC}')
                phone = input('Enter phone number: ')
                try:
                    Phone(phone)
                    break
                except:
                    print(f"{bcolors.FAIL}Incorrect value{bcolors.ENDC}")
                    continue 
            el.add_phone(phone)
            print(f"Phone has been added to contact {bcolors.OKBLUE}{name}{bcolors.ENDC}")
            close(contact_book)
            return 'added'
    print(f'There is not contact witn name {bcolors.FAIL}{name}{bcolors.ENDC} in the contact book ' )  


def change(contact_book: AddressBook):
    while True:
        print('Phone number must be in Contact book')
        print(f'Example phone number: {bcolors.OKGREEN}1234525680{bcolors.ENDC}')
        phone = input('Enter phone number:  ')
        try:
            Phone(phone)
            break
        except:
            print(f"{bcolors.FAIL}Incorrect value{bcolors.ENDC}")
            continue
    for phone_contact_book in contact_book.data.values():
        for tel in phone_contact_book.phones:
            if phone == tel.value:
                while True:
                    new_phone = input('Enter new phone number:  ')
                    try:
                        Phone(new_phone)
                        break
                    except:
                        print(f"{bcolors.FAIL}Incorrect value{bcolors.ENDC}")
                        continue
                phone_contact_book.edit_phone(phone, new_phone)
                print(f"Phone number {bcolors.OKBLUE}{phone}{bcolors.ENDC} has been replaced by {bcolors.OKGREEN}{new_phone}{bcolors.ENDC}")
                close(contact_book)
                return 'changed'
    print(f'There is not {bcolors.FAIL}{phone}{bcolors.ENDC} phone number in the contact book '  )     


def show(contact_book: AddressBook):
    res = contact_book.list_contacts()
    res2 = (' ;\n').join(res)
    print(res2)


def start():
    if Path(CONTACTS_FILE_NAME).is_file():
        return AddressBook.load_from_file(CONTACTS_FILE_NAME)
    else:
        return AddressBook()




def edit_email(contact_book: AddressBook):
    while True:
        name = input('Enter contact name:   ')
        if name.isalpha():
            break
        else:
            print(f"{bcolors.FAIL}Incorrect value{bcolors.ENDC}")
    for el in contact_book.data.values():
        if name == el.name.value:
            while True:
                email = input('Enter email:  ')
                try:
                    Email(email)
                    break
                except:
                    print(f"{bcolors.FAIL}Incorrect value{bcolors.ENDC}")
                    continue
            el.edit_email(email)
            close(contact_book)
            return  "Email edited successfully"   
    print(f'There is not contact witn name {bcolors.FAIL}{name}{bcolors.ENDC} in the contact book ' )    


def edit_birthday(contact_book: AddressBook):
    while True:
        name = input('Enter contact name:   ')
        if name.isalpha():
            break
        else:
            print(f"{bcolors.FAIL}Incorrect value{bcolors.ENDC}")
    
    for el in contact_book.data.values():
        if name == el.name.value:
            while True:
                print(f'Example birthday: {bcolors.OKGREEN}12-01-1991{bcolors.ENDC}')
                birthday = input('Enter birthday:   ')
                if birthday == '':
                    birthday = None
                    break
                try:
                    Birthday(birthday)
                    break
                except:
                    print(f"{bcolors.FAIL}Incorrect value{bcolors.ENDC}")
                    continue
            el.edit_birthday(birthday)
            close(contact_book)
            return 'done'
    print(f'There is not contact witn name {bcolors.FAIL}{name}{bcolors.ENDC} in the contact book ' )  


def edit_address(contact_book: AddressBook):
    while True:
        name = input('Enter contact name   ')
        if name.isalpha():
            break
        else:
            print(f"{bcolors.FAIL}Incorrect value{bcolors.ENDC}")
    for el in contact_book.data.values():
        if name == el.name.value:
            address = input('Enter address  ')
            el.edit_address(address)
            close(contact_book)
            return  "Email edited successfully"   
    print(f'There is not contact witn name {bcolors.FAIL}{name}{bcolors.ENDC} in the contact book ' )  


def remove_phone(contact_book: AddressBook):
    while True:
        name = input('Enter contact name   ')
        if name.isalpha():
            break
        else:
            print(f"{bcolors.FAIL}Incorrect value{bcolors.ENDC}")
    for el in contact_book.data.values():
        if name == el.name.value:
            while True:
                phone = input('Enter phone number  ')
                try:
                    Phone(phone)
                    break
                except:
                    print(f"{bcolors.FAIL}Incorrect value{bcolors.ENDC}")
                    continue
            print( f"Phone number {bcolors.FAIL}{phone}{bcolors.ENDC} removed successfully")
            el.remove_phone(phone) 
            close(contact_book) 
            return 'done'        
    print(f'There is not contact witn name {bcolors.FAIL}{name}{bcolors.ENDC} in the contact book ' )  
 

def remove_email(contact_book: AddressBook):
    while True:
        name = input('Enter name   ')
        if name.isalpha():
            break
        else:
            print(f"{bcolors.FAIL}Incorrect value{bcolors.ENDC}")
    for el in contact_book.data.values():
        if name == el.name.value:
            el.remove_email()
            close(contact_book)
            return 'done'          
    print(f'There is not contact witn name {bcolors.FAIL}{name}{bcolors.ENDC} in the contact book ' )   


def remove_address(contact_book: AddressBook):
    while True:
        name = input('Enter contact name:   ')
        if name.isalpha():
            break
        else:
            print(f"{bcolors.FAIL}Incorrect value{bcolors.ENDC}")
    for el in contact_book.data.values():
        if name == el.name.value:
            el.remove_address()
            close(contact_book)
            return 'removed'         
    print(f'There is not contact witn name {bcolors.FAIL}{name}{bcolors.ENDC} in the contact book ' )   


def remove_birthday(contact_book: AddressBook):
    while True:
        name = input('Enter name:   ')
        if name.isalpha():
            break
        else:
            print(f"{bcolors.FAIL}Incorrect value{bcolors.ENDC}")
    for el in contact_book.data.values():
        if name == el.name.value:
            el.remove_birthday()   
            close(contact_book)
            return 'done'     
    print(f'There is not contact witn name {bcolors.FAIL}{name}{bcolors.ENDC} in the contact book ' )   


def find_contact(contact_book: AddressBook):
    while True:
        name = input('Enter name: ')
        if name.isalpha():
            break
        else:
            print(f"{bcolors.FAIL}Incorrect value{bcolors.ENDC}")
    contact_book.find(name)   


def remove_contact(contact_book: AddressBook):
    while True:
        name = input('Enter name:   ')
        if name.isalpha():
            break
        else:
            print(f"{bcolors.FAIL}Incorrect value{bcolors.ENDC}")
    contact_book.delete(name) 
    close(contact_book)


'''def birthdays(contact_book: AddressBook):
    while True:
        quant = input('Enter quantity of days:   ')
        if quant.isdigit() and 0 < int(quant) < 365:
            break    
        else:
            print('Incorrect value')
    print(contact_book.contacts_birthdays(quant) ) '''   


def search(contact_book: AddressBook):
    inf = input('Enter information about contact:   ') 
    print(contact_book.search(inf))



