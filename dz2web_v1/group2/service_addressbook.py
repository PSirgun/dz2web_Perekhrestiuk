from .addressbook import Name, Phone, Record, AddressBook, Birthday
from datetime import datetime
import re
from .display import AddressBookConsoleInterface

book = AddressBook()
book.load()
console_interface = AddressBookConsoleInterface(book)

def user_error(func):
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return "Not enough params. Use help."
        except KeyError:
            return "Unknown rec_id. Try another or use help."
        except ValueError:
            return "Unknown or wrong format. Check phone and/or birthday"
        except AttributeError:
            return "Contacts was not found"

    return inner



def func_hello(*args):
    return f"How can I help you?"

@user_error
def func_add(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    if book.find(name.value):
        raise ValueError    
    contact = Record(name)
    contact.phones.add_phone(phone)
    book.add_record(contact) 
    return console_interface.display_added_inf(name.value, phone.value)

@user_error
def func_add_phone(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    contact = book.find(name.value)
    contact.phones.add_phone(phone)
    return console_interface.display_added_inf(name.value, phone.value)

@user_error
def func_edit_phone(*args):
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    book.find(name.value).phones.edit_phone(old_phone, new_phone)
    return console_interface.display_added_inf(name.value, new_phone=new_phone.value, old_phone=old_phone)

@user_error
def func_remove_phone(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    book.find(name.value).phones.remove_phone(phone)
    return console_interface.display_added_inf(name.value, old_phone=phone)
# @user_error
# def func_show_all(*args):
#     line = ""
#     for record in book:
#         line += f"{record}\n"
#     return line

@user_error
def func_show_all(*args):
    return console_interface.display_contacts()

@user_error
def func_show(*args):
    for page in book.iterator(int(args[0]) if args else None):
        for line in page:
            print(console_interface.display_one_contact(line))
        print("End page\n")
    return "End phone book"

@user_error
def func_add_birthday(*args):
    name = Name(args[0])
    bd = Birthday(args[1:])
    if book.find(name):
        contact:Record = book[name]
        contact.birthday.add_birthday(bd)
    else:
        raise AttributeError
    return console_interface.display_added_inf(name, birthday=bd)

@user_error
def func_when_birthday(*args):
    name = Name(args[0]).value
    result = book.find(name).birthday.days_to_birthday()
    return console_interface.display_added_inf(name, days_to_bd=result)

@user_error
def func_find(*args):
    for key, data in book.data.items():
        data:Record
        if data.find_in(args[0]):
            console_interface.display_one_contact(key)
    
    return "ok"



@user_error
def func_remove(*args):
    rec_id = args[0]
    book.delete(rec_id)
    return f"Contact {rec_id} succesfully removed"




def unknown(*args):
    return "Unknown command. Try again or use help."









