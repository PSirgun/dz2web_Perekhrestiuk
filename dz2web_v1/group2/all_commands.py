from .service_addressbook import *
from .service_notebook import *
from . import help_func
from . import sort
def func_good_bye():
    book.save()
    note_book.save_data()
    print(f"Good bye!")
    exit()

book_commands = {
    "hello": func_hello,
    "add": func_add,
    "add phone": func_add_phone,
    "add birthday": func_add_birthday,
    "edit phone": func_edit_phone,
    "show all records": func_show_all,
    "show records": func_show,
    "find record": func_find,
    "delete record": func_remove,
    "delete phone": func_remove_phone,
    "sort folder": sort.func_sort_folder,
    "when birthday": func_when_birthday,
    "help": help_func.func_help,
    "": unknown
    
}

note_commands = {
    "add note": func_add_note,  # add note заголовок нотатку --> далі по підказкам
    "add tags": func_add_tags,  # add tags заголовок --> додасть нові теги до уже існуючих
    "edit note": func_edit_note,  # edit note заголовок --> далі по підказкам
    "edit tags": func_edit_tags,  # edit tags заголовок --> далі по підказкам
    "show notes": func_show_notes,  # show notes  (тут без заголовку)
    "find note": func_search_notes,  # show note (будь яку слово з заголовку або #тег)
    "sort notes": func_sort_notes,  # sort notes (без аргументів) - сортує, виводить та зберігає новий порядок нотатків, сортування за кількістю тегів, як замовляв викладач
    "delete notes": func_delete_notes,  # якщо вказати заголовок, то видалиться запис, якщо без аргументів, то видаляться всі записи, після підтвердження видалення
}

exit_input = ["good bye", "close", "exit"]
exit_commands = {command: func_good_bye for command in exit_input}



COMMANDS = {}
COMMANDS.update(exit_commands)
COMMANDS.update(note_commands)
COMMANDS.update(book_commands)
COMMANDS = dict(sorted(COMMANDS.items(), reverse=True))