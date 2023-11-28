from collections import UserDict, OrderedDict
from pathlib import Path
import pickle

class NoteBook(UserDict):
    
    def find(self, title):
        if title in self.keys():
            found_rec = self.get(title)
            return found_rec
        raise KeyError
    
    def input_t(seld, prompt):
        lines = []
        print(prompt)
        while True:
            line = input()
            if line.lower() == "save":
                break
            lines.append(line)
        return "\n".join(lines)


    def args_to_title(self, args=None):
        if not args:
            raise IndexError
        title = " ".join(args)
        if title not in self.data:
            raise KeyError
        return title

    def add_note(self, title, text, tags=None):
        if tags is None:
            tags = []
        self.data[title] = {"text": text, "tags": tags}

    def edit_note(self, title, new_text=None, new_tags=None):
        if title in self.data:
            if new_text:
                self.data[title]["text"] = new_text
            if new_tags is not None:
                self.data[title]["tags"] = new_tags

    def delete_note(self, title=None):
        if title in self.data:
            del self.data[title]
        if not title:
            self.data.clear()

    def search_notes(self, keyword):
        page = []
        keyword = keyword.lower()
        for title, note in self.data.items():
            if keyword in title.lower() or any(
                keyword in tag.lower() for tag in note["tags"]
            ):
                page.append(title)
        return page

    def sort_notes(self):
        sorted_data = sorted(
            self.data.items(), key=lambda x: (-len(x[1]["tags"]), x[0])
        )
        self.data = OrderedDict(sorted_data)


    def load_data(self):
        file_name = "note.bin"
        try:
            load_dir = Path(__file__).resolve().parent
            file_path = load_dir.joinpath(file_name)
            with open(file_path, "rb") as fb:
                self.data = pickle.load(fb)
                print(
                    f"\033[32mNoteBook with {len(self.data)} notes is succesfuly uploaded\033[0m"
                )
                return self.data
        except FileNotFoundError:
            book = NoteBook()

    def save_data(self):
        file_name = "note.bin"
        save_dir = Path(__file__).resolve().parent
        file_path = save_dir.joinpath(file_name)
        with open(file_path, "wb") as fb:
            pickle.dump(self.data, fb)
            print("\033[32mNoteBook is saved as note.bin\033[0m")
        return None
