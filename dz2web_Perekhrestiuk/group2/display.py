from abc import ABC, abstractmethod
from .addressbook import AddressBook
from .notebook import NoteBook

class AbstractAddressBook(ABC):
    @abstractmethod
    def display_contacts(self, contacts):
        pass  
    
    
    @abstractmethod
    def display_one_contact(self, name):
        pass


    @abstractmethod
    def display_added_inf(self, name):
        pass  



class AddressBookConsoleInterface(AbstractAddressBook):
    def __init__(self, address_book:AddressBook):
        self.address_book = address_book

    def display_contacts(self):
        all_result = ''
        for contact in self.address_book.data:
            selected_contact = self.address_book.find(contact)
            result = "Name: {}\nPhones: {}\nBirthday: {}\n".format(
                selected_contact.name.value,
                ', '.join(str(phone) for phone in selected_contact.phones.values),
                selected_contact.birthday
            )

            all_result += f"{result}\n"
        return all_result

        
    def display_one_contact(self, name):
        selected_contact = self.address_book.find(name)
        if selected_contact:
            result = "Name: {}\nPhones: {}\nBirthday: {}\n".format(
                selected_contact.name.value,
                ', '.join(str(phone) for phone in selected_contact.phones.values),
                selected_contact.birthday
            )
            return result
        else:
            return f"Contact with name {name} not found."
        
    def display_added_inf(self, name, new_phone=None, old_phone=None, birthday=None, days_to_bd=None ):
        selected_contact = self.address_book.find(name)
        result = f"To contact {name}, "
        if new_phone:
            result += f"added Phone: {selected_contact.phones.values[-1]} "
        if birthday:
            result += f"added Birthday: {selected_contact.birthday} " 
        if old_phone:
            result += f"removed Phone: {selected_contact.birthday} " 
        if days_to_bd:
            result  += f"left {days_to_bd} to birthday "
            return result
        result += "in address book"
        return result


class AbstractNoteBook(ABC):
    @abstractmethod
    def display_notes(self):
        pass

    @abstractmethod
    def display_one_note(self):
        pass

    @abstractmethod
    def display_added_inf(self):
        pass

class NoteBookConsoleInterface(AbstractNoteBook):
    def __init__(self, note_book:NoteBook):
        self.note_book = note_book
        self.text = 'text'
        self.tags = 'tags'
    
    def display_notes(self, ):
        result = ""
        for title, note in self.note_book.data.items():
            result += (
                "\n\033[34m<<<{}>>>\033[0m\n{}\n\033[34mtags:\033[0m {}\n".format(
                    title, note["text"], note["tags"]
                )
            )
        return result

    def display_one_note(self, title):
            selected_note = self.note_book.find(title)
            return "\n\033[34m<<<{}>>>\033[0m\n{}\n\033[34mtags:\033[0m {}\n".format(
                title, selected_note[self.text], selected_note[self.tags]
            )

    def display_added_inf(self, title, tags=None):
        selected_note = self.note_book.find(title)
        result = f'Note with title: {title} '
        if tags:
            tags_str = " ".join(x for x in selected_note[self.tags])
            result += f'and tags {tags_str} '
        result += "was saved"
        return result




if __name__ == '__main__':
    note_book = NoteBook()
    note_book.load_data()
    aa = NoteBookConsoleInterface(note_book)
    aa.display_added_inf("aasd")