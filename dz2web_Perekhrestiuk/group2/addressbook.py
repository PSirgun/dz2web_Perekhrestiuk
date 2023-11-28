from collections import UserDict
from collections.abc import Iterator
from datetime import datetime
from pathlib import Path
import pickle
import re


class Field:
    def __init__(self):
        self.__value = None

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value

class FindContext:
    def find_in(self, search_value):
        raise NotImplementedError

class Name(Field, FindContext):
    def __init__(self, value):
        super().__init__()
        self.value = value
    
    def __repr__(self):
        return self.value
    
    def find_in(self, search_value):
        return search_value in self.value
    



class Phone(Field):
    def __init__(self, value):
        self.value = value
        
    def phone_validator(self, phone):
        new_phone = (
        phone.strip()
        .removeprefix("+38")
        .replace("(", "")
        .replace(")", "")
        .replace("-", "")
        .replace(" ", "")
    )
        if len(new_phone) != 10 or not new_phone.isdigit():
            raise ValueError
        return new_phone
    
    def __repr__(self):
        return self.__value
    

    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = self.phone_validator(new_value)

class ObjPhones(FindContext):  
    def __init__(self):   
        self.values = []

    def add_phone(self, new_phone):
        self.values.append(new_phone)

    def edit_phone(self, old_phone: Phone, new_phone: Phone):
        if any(phone.value == old_phone.value for phone in self.values):
            self.remove_phone(old_phone)
            self.values.append(new_phone)


    def remove_phone(self, phone_number: str):
        for phone in self.values:
            if phone.value == phone_number.value:
                self.values.remove(phone)
                break
    
    def __str__(self) -> str:
        return f'{self.values}'
    
    def find_in(self, search_value):
        return any(search_value in phone.value for phone in self.values)
    
class Birthday:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        new_value = str(new_value)
        new_value = re.findall(r"\d+", new_value)
        new_value = " ".join(i for i in new_value)
        new_value = datetime.strptime(new_value, '%d %m %Y')
        self._value = new_value
        


 
    
    def __iter__(self):
        yield self._value.strftime('%Y-%m-%d') 



class ObjBirthday(FindContext):
    def __init__(self) -> None:
        self.birthday = None    
    
    def add_birthday(self, birthday):
        self.birthday = birthday

    def days_to_birthday(self):
        today = datetime.today().date()
        next_bd = self.birthday._value.replace(year=today.year)
        next_bd = next_bd.date()
        if next_bd < today:
            next_bd = next_bd.replace(year=today.year + 1)
        days_left = (next_bd - today).days
        return days_left
    
    def find_in(self, search_value):
        return search_value in self.birthday._value.strftime('%d-%m-%Y')
              
    def __repr__(self):
        if not self.birthday:
            return "N/A"
        return self.birthday._value.strftime('%d-%m-%Y')  
    
    def find_in(self, search_value):
        if self.birthday:
            return search_value in self.birthday._value.strftime('%d-%m-%Y')
        return False

class Record(FindContext):
    def __init__(self, name: Name):
        self.name = name
        self.phones = ObjPhones()
        self.birthday = ObjBirthday()

    def find_in(self, search_value):
        return (
            self.name.find_in(search_value)
            or self.phones.find_in(search_value)
            or self.birthday.find_in(search_value)
        )

class AddressBook(UserDict):
    __instance = None
    def __init__(self):
        super().__init__()
        self.__lines = 2
        

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def add_record(self, record: Record):
        self[str(record.name)] = record

    def find(self, name) -> Record:
        if name in self.keys():
            found_rec = self.get(name)
            return found_rec

    def delete(self, name):
        if name in self.keys():
            self.pop(name)

    def iterator(self, lines):
        if lines is None:
            lines = self.__lines
        else:
            self.__lines = lines
        count = 0
        page = []
        for items in self.data:
            page.append(items)
            count += 1
            if count == lines:
                yield page
                page = []
                count = 0
        if page:
            yield page

    def load(self):
        file_name = "book.bin"
        try:
            load_dir = Path(__file__).resolve().parent
            file_path = load_dir.joinpath(file_name)
            with open(file_path, "rb") as fb:
                self.data = pickle.load(fb)
                print(
                    f"\033[32mAddressBook with {len(self.data)} contacts is succesfuly uploaded\033[0m"
                )
                return self.data
        except FileNotFoundError:
            book = AddressBook()

    def save(self):
        file_name = "book.bin"
        save_dir = Path(__file__).resolve().parent
        file_path = save_dir.joinpath(file_name)
        with open(file_path, "wb") as fb:
            pickle.dump(self.data, fb)
            print("\033[32mAddressBook is saved as book.bin\033[0m")
        return None

